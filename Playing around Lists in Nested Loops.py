from typing import List
import math
def area_triangles(dimension_list: List[list]) -> List[int]:
    '''Returns the new list of areas of triangles
    Here, 
    index = 0 refers to the length of  left side of the triangle
    index = 1 refer to the length of the base of the triangle
    index = 2 refers to the length of the right side of the triangle.
    
    area_triangles([10, 20, 30], [40, 50, 60], [60, 70, 80])
    [0.0, 780.6247497997997, 1705.6890103415687]
    
    '''

    area_triangles = []
    
    for dimension in dimension_list:
        for area in dimension:
            area = 0.5 * dimension[1] * (math.sqrt((dimension[0] ** 2) - (dimension[1] / 2) ** 2))
            
        area_triangles.append(area)
        
    return area_triangles

from typing import List

def sum_list(value_sets: List[list]) -> List[int]:
    '''Returns a new list containing the sum of the lists at each index of the list.'''
    
    sum_list = []
    
    for sum_groups in value_sets:
       
        total = 0
        for value in sum_groups:
            total = total + value
        
        sum_list.append(total)
    
    return sum_list
  