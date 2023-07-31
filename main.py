import string

def find4LargestLexSubstringsOfLength5(txt_file):
    
    with open(txt_file) as f:
        txt = f.readlines()

    # clean input
    txt = [x.replace('\n', '') for x in txt]
    txt = [x.lower() for x in txt]

    # the only imported package is 'string' but could be ommited by specifying alphanums manually
    alphanums = sorted(string.ascii_lowercase +  string.digits, reverse=True)

    # containers for data of lexicographically largest substrings of length 5
    top_strings = []
    top_string_lines = []
    top_string_start_indexes = []

    # main optimization: search for lexicographically largest substring by finding locations of the 
    # alphanumericals in decreasing order
    for curr_alphanum in alphanums:

        if len(top_strings) >= 4:
            sort_index = [i for i, x in sorted(enumerate(top_strings), key=lambda x: x[1], reverse=True)]
            top_strings = [top_strings[x] for x in sort_index[:4]]
            top_string_lines = [top_string_lines[x] for x in sort_index[:4]]
            top_string_start_indexes = [top_string_start_indexes[x] for x in sort_index[:4]]
            break

        for iter_line, txt_line in enumerate(txt):
            # find all occurences of current alphanumerical
            curr_alphanum_inds = [x for x in range(len(txt_line)) if txt_line[x] == curr_alphanum]

            if curr_alphanum_inds:

                # get substrings
                substrings = [txt_line[x:x+5] for x in curr_alphanum_inds]
                if len(substrings[-1]) < 5:
                    curr_alphanum_inds.pop(-1)
                    substrings.pop(-1)

                # remove substring if it doesn't comprise purely of alphanumericals
                to_be_removed = [i for i, x in enumerate(substrings) if not x.isalnum()]
                [curr_alphanum_inds.pop(i) for i in reversed(to_be_removed)]

                
                if len(curr_alphanum_inds) > 1:
                    dist = [x - y for x, y in zip(curr_alphanum_inds[1:], curr_alphanum_inds[:-1])]

                    # resolve overlapping substrings    
                    while any([x < 5 for x in dist]):
                        ind_overlap = [i for i, x in enumerate(dist) if x < 5]

                        left_substring_ind = curr_alphanum_inds[ind_overlap[0]]
                        right_substring_ind = curr_alphanum_inds[ind_overlap[0]+1]

                        left_substring = txt_line[left_substring_ind:left_substring_ind+5]
                        right_substring = txt_line[right_substring_ind:right_substring_ind+5]

                        if left_substring > right_substring:
                            curr_alphanum_inds.pop(1)
                        else:
                            curr_alphanum_inds.pop(0)

                        dist = [x - y for x, y in zip(curr_alphanum_inds[1:], curr_alphanum_inds[:-1])]


                substrings = [txt_line[x:x+5] for x in curr_alphanum_inds]

                if substrings:
                    top_string_lines.extend([iter_line]*len(substrings))
                    top_string_start_indexes.extend(curr_alphanum_inds)
                    top_strings.extend(substrings)

    # convert line and start index data to coords
    coords = [[x, y, 0] for x, y in zip(top_string_lines, top_string_start_indexes)]

    return top_strings, coords

def computeQuadAreaBasedOnVertices(coords):
    
    # possible triangles that can be made of 4 vertices
    tri = [[0, 1, 2], [0, 1, 3], [0, 2, 3], [1, 2, 3]]
    tri_areas = [None]*4
    
    # compute area of each possible triangle using cross product
    for i, x in enumerate(tri):
        v1 = [coords[tri[i][1]][0] - coords[tri[i][0]][0], coords[tri[i][1]][1] - coords[tri[i][0]][1]]
        v2 = [coords[tri[i][2]][0] - coords[tri[i][0]][0], coords[tri[i][2]][1] - coords[tri[i][0]][1]]
        tri_areas[i] = 0.5 * abs(v1[0] * v2[1] - v2[0] * v1[1])

    sorted_tri_areas = sorted(tri_areas)
    
    # case 1: quad with 3 colinear vertices
    if not all(sorted_tri_areas):
        output_area = sorted_tri_areas[:3]
        print(f'Area: {output_area}.')
    # case 2: set of vertices can form 3 different concave quads
    elif sorted_tri_areas[-1] == sum(sorted_tri_areas[:-1]):
        output_area = [ 
            sorted_tri_areas[0] + sorted_tri_areas[1],  
            sorted_tri_areas[1] + sorted_tri_areas[2], 
            sorted_tri_areas[0] + sorted_tri_areas[2] 
        ]

        print(f'There are three possible quads for this set of vertices - they have the following areas: {output_area}.')
    # case 3: reguler, convex quad
    else:
        output_area = 0.5 * sum(sorted_tri_areas)
        print(f'Area: {output_area}.')


    return output_area

        
if __name__ == "__main__":

    (substrings, coords) = find4LargestLexSubstringsOfLength5('text.txt')
    print(f'The top strings are:{substrings}')

    quad_area = computeQuadAreaBasedOnVertices(coords)


