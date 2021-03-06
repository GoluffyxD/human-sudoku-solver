
import copy
from texttable import Texttable

pos={0:(0,0),1:(0,3),2:(0,6),3:(3,0),4:(3,3),5:(3,6),6:(6,0),7:(6,3),8:(6,6)}

sudoku1=[   
        [0, 0, 0, 2, 6, 0, 7, 0, 1], 
        [6, 8, 0, 0, 7, 0, 0, 9, 0],
        [1, 9, 0, 0, 0, 4, 5, 0, 0], 
        [8, 2, 0, 1, 0, 0, 0, 4, 0], 
        [0, 0, 4, 6, 0, 2, 9, 0, 0], 
        [0, 5, 0, 0, 0, 3, 0, 2, 8], 
        [0, 0, 9, 3, 0, 0, 0, 7, 4], 
        [0, 4, 0, 0, 5, 0, 0, 3, 6], 
        [7, 0, 3, 0, 1, 8, 0, 0, 0]
        ]
sudoku2 =[
        [0,0,7,0,0,0,0,0,4],
        [0,0,0,6,5,0,0,0,2],
        [0,2,0,8,0,1,0,6,0],
        [0,1,0,0,0,0,0,0,0],
        [0,0,0,0,4,0,7,8,5],
        [5,0,2,0,0,0,0,0,0],       
        [1,0,0,0,0,0,0,0,0],
        [0,9,4,0,0,0,0,0,0],
        [0,0,0,9,2,0,0,0,6]
        ]
sudoku3 = [
        [1,0,0,7,0,0,0,2,3],
        [0,2,0,0,0,0,0,7,1],
        [0,0,9,0,0,4,0,0,0],
        [9,0,0,0,3,6,0,8,0],
        [7,0,6,0,0,0,0,0,0],
        [0,0,0,0,0,0,5,0,0],
        [0,0,0,0,0,0,0,5,0],
        [0,0,0,0,5,0,0,0,7],
        [4,0,3,0,1,0,0,0,0]
]

def chkPossible(mat,x,y,val):
    if val in mat[x][:]:
        return False
    if val in [temp[y] for temp in mat ]:
        return False
    posKey= 3*(x//3) + y//3
    (startx,starty)=pos[posKey]
    for i in range(startx,startx+3):
        for j in range(starty,starty+3):
            if mat[i][j]== val:
                return False
    return True

def getChoiceMatrix(mat):
    possible=[]
    for i in range(9):
        temp=[]
        for j in range(9):
            if mat[i][j]==0:
                temp.append([vals for vals in range(1,10) if chkPossible(mat,i,j,vals)])
            else:
                temp.append([])
        possible.append(temp)
    print("Initial Choice Matrix")
    printChoiceMatrix(possible,mat)
    while True:
        reduced = reduceChoiceMatrix(possible)
        if possible == reduced:
            print("Broke out of loop! No further reductions possible")
            break
        else:
            possible = reduced
        print("After:")
        printChoiceMatrix(possible,mat)
    return possible

def chkZero(mat):
    for i in mat:
        if 0 in i:
            return True
    return False

def printChoiceMatrix(possible,mat):
    t=Texttable()
    for i in range(9):
        row=[]
        for j in range(9):
            if possible[i][j]==[]:
                row.append(mat[i][j])
            else:
                str1 = 'c'+ '('+ ",".join([str(i) for i in possible[i][j]])+')'
                row.append(str1)
        t.add_row(row)
    print(t.draw())

def reduceChoiceMatrix(possible_par):
    possible = copy.deepcopy(possible_par)
    #Row Reduce
    # temp = possib#le.copy()
    for i in range(9):
        freq={}
        for j in range(9):
            if possible[i][j]!=[]:
                if tuple(possible[i][j]) in freq.keys():
                    freq[tuple(possible[i][j])]+=1
                else:
                    freq[tuple(possible[i][j])]=1
        for el in freq.keys():
            if freq[el]>1 and freq[el]==len(el):
                for m in range(9):
                    if len(possible[i][m])>len(el):
                        print("Removing {} across row {} choices".format(el,i))
                        for val in el:
                            if val in possible[i][m]:
                                try:
                                    possible[i][m].remove(val)
                                except:
                                    pass
    
    # Column Reduce
    for i in range(9):
        freq={}
        for j in range(9):
            if possible[j][i]!=[]:
                if tuple(possible[j][i]) in freq.keys():
                    freq[tuple(possible[j][i])]+=1
                else:
                    freq[tuple(possible[j][i])]=1
        # del freq[()]
        for el in freq.keys():
            if freq[el]>1 and freq[el]==len(el):
                for m in range(9):
                    if len(possible[m][i])>len(el):
                        print("Removing {} across column {} choices".format(el,i))
                        for val in el:
                            if val in possible[m][i]:
                                try:
                                    possible[m][i].remove(val)
                                except:
                                    pass
    
    # Small Square Reduce
    for i in range(9):
        (startx,starty)=pos[i]
        freq={}
        for k in range(startx,startx+3):
            for l in range(starty,starty+3):
                if possible[k][l]!=[]:
                    if tuple(possible[k][l]) in freq.keys():
                        freq[tuple(possible[k][l])]+=1
                    else:
                        freq[tuple(possible[k][l])]=1
        # del freq[()]
        for el in freq.keys():
            if freq[el]>1 and freq[el]==len(el):
                for k in range(startx,startx+3):
                    for l in range(starty,starty+3):
                        if len(possible[k][l])>len(el):
                            print("Removing {} in small square {} choices".format(el,i))
                            for val in el:
                                if val in possible[k][l]:
                                    try:
                                        possible[k][l].remove(val)
                                    except:
                                        pass
    
    # Remove assumptions from small square
    for i in range(9):
        (startx,starty)=pos[i]
        for vals in range(1,10):
            xpos=set()
            ypos=set()
            for k in range(startx,startx+3):
                for l in range(starty,starty+3):
                    if vals in possible[k][l]:
                        xpos.add(k)
                        ypos.add(l)
            # print("square: ",i,"vals: ",vals,"xpos:",xpos,"ypos:",ypos)
            if len(xpos)==1:
                for ik in xpos:
                    el = ik
                for rowel in range(9):
                    if rowel in range(starty,starty+3):
                        continue
                    if vals in possible[el][rowel]:
                        try:
                            possible[el][rowel].remove(vals)
                        except:
                            pass
            elif len(ypos)==1:
                # print(ypos,i)
                for ik in ypos:
                    el = ik
                    # print(el)
                for colel in range(9):
                    if colel in range(startx,startx+3):
                        continue
                    if vals in possible[colel][el]:
                        try:
                            possible[colel][el].remove(vals)
                        except:
                            pass

    
    
    return possible
