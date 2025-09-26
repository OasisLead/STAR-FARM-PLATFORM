context_window1_struct = ("This is the last part of the output. Don't make any chain of thought or reasoning for this phase and please directly generate the JSON format I ask you here right under. This JSON format should contain, for each practice (practice 1 and practice 2), a list of different possible rotations over a year. The rotations should be lists of string of crops in the right order, the rotations lists should be stored in a list for each pratice, and they can contain as many crops as can be rotated within a year over a single plot as long at is makes sense. If there is a case where two crops/species/living beings are cultivated over the same plot at the same time (Call them specie 1 and specie 2), then you can write it as a single element of the list, as the string named ""specie 1 and specie 2""  \n" 

#"For example, for the practice Triple rice, give multiple lists of possible crop combinations like :" 
#": [[rice_species1, rice_species2, rice_species3],[rice_species4,rice_species2,rice_species6]]." 

"This is the specific format I would like you to use for the final output of the answer: \n\n"

"class CropCycle(BaseModel): \n" 
"crops_rotation_list_practice_1: List[List[str]]\n"
"crops_rotation_list_practice_2: List[List[str]]\n\n"

"Where the strings are the names of the species, or more names if they are grown on the same plot during the same period " 

"now just prompt it directly")

print(context_window1_struct)