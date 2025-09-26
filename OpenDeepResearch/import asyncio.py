import asyncio
import sys
from io import StringIO
from contextlib import redirect_stdout
import threading
import queue

# Add this new class for capturing output
class ThreadSafeOutput:
    def __init__(self):
        self.outputs = {}
        self.lock = threading.Lock()
        
    def store_output(self, thread_id, output):
        with self.lock:
            if thread_id not in self.outputs:
                self.outputs[thread_id] = []
            self.outputs[thread_id].append(output)
            
    def get_all_outputs(self):
        with self.lock:
            return dict(self.outputs)

# Modify the deep_search_report to capture its output
async def async_deep_search_report(query, thread_id, output_manager, temperature=0.2, max_retries=3):
    # Capture stdout
    string_io = StringIO()
    with redirect_stdout(string_io):
        try:
            result = deep_search_report(query, temperature, max_retries)
            captured_output = string_io.getvalue()
            output_manager.store_output(thread_id, captured_output)
            return result
        except Exception as e:
            output_manager.store_output(thread_id, f"Error in thread {thread_id}: {str(e)}")
            raise e

# New function to run multiple searches in parallel
async def run_parallel_searches(queries):
    output_manager = ThreadSafeOutput()
    tasks = []
    
    for i, query in enumerate(queries):
        task = asyncio.create_task(
            async_deep_search_report(query, f"Search_{i+1}", output_manager)
        )
        tasks.append(task)
    
    results = await asyncio.gather(*tasks, return_exceptions=True)
    
    # Print all captured outputs
    all_outputs = output_manager.get_all_outputs()
    for thread_id, outputs in all_outputs.items():
        print(f"\n=== Output from {thread_id} ===")
        for output in outputs:
            print(output)
            
    return results

# Modified main execution
if __name__ == "__main__":
    # Example queries
    queries = [
        """Query 1: Agricultural practices in Region A...""",
        """Query 2: Agricultural practices in Region B..."""
    ]
    
    # Run searches in parallel
    results = asyncio.run(run_parallel_searches(queries))
    
    # Print results
    for i, result in enumerate(results):
        print(f"\n=== Result from Search {i+1} ===")
        print(result)



if __name__ == "__main__":
    # Get multiple inputs
    inputs1 = get_user_input_1()
    inputs2 = get_user_input_1()
    
    queries = [
        generate_query_1(inputs1),
        generate_query_1(inputs2)
    ]
    
    # Run parallel searches
    results = asyncio.run(run_parallel_searches(queries))
    
    # Print results
    for i, result in enumerate(results):
        print(f"\n=== Generated Report {i+1} ===\n")
        print(result)