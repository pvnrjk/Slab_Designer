

from glob import glob
import math

length = float(input("Enter the length of the slab in m = "))
breadth = float(input("Enter the breadth of the slab in m = "))
gradeConcrete = float(input("Enter the Grade of cement N/mm2 = "))
gradeSteel = float(input("Enter the Grade of Steel N/mm2 = "))
liveLoad = float(input("Enter the live load kN/m2 = "))
clearCover = float(input("Enter the Clear cover to be provided in mm = "))
barDia = float(input("Enter the Bar dia in mm = "))

# Check the Slab
def Check_Slab():
    global lybylx
    lybylx = length/breadth
    global typeSlab
    if(lybylx>2):
        typeSlab = "One Way Slab"
        print('One Way Slab')
    else:
        typeSlab = "Two Way Slab"
        print("Two Way Slab")
    print(f"ly/lx ={lybylx}")
    print("\n")

# Depth Calculation  
def Effective_Depth():
    print("Refer page Number - 38, Fig - 4, \n Ratio of steel Provide = 1,")
    fs = 0.58 * gradeSteel * 1 
    print("Percentage Tension Reinforcement Assumed = 0.4 %")
    print("Interpolate and Enter the MF")
    print(f"fs = {fs} and pt = 0.4%")
    MF = float(input("Enter the modification factor = "))
    if(breadth<=3.5 and liveLoad<=3):
        if(gradeSteel==250):
            spanbydepth = 35 * MF 
        else:
            spanbydepth = 35 * MF * 0.8
    else:
        spanbydepth = 20 * MF 
    
    calEffectiveDepth = breadth*1000 / spanbydepth 
    print(f"Calculated Effective Depth = {calEffectiveDepth} mm")
    global effectiveDepth
    effectiveDepth = float(input("Enter the approx effective depth in mm = "))
    print(f"Effective Depth = {effectiveDepth} mm")
    calDepth = effectiveDepth + clearCover + barDia/2 
    print(f"Calculated Depth = {calDepth} mm")
    global Depth
    Depth = float(input("Enter the approx depth in mm = "))
    print(f"Depth = {Depth} mm")
    print("\n")

# Effective Span 
def Effective_Span():
    global lx 
    lx = breadth + effectiveDepth/1000
    global ly 
    ly = length + effectiveDepth/1000
    print("\n")

# Load Calculations 
def Load_Calculation():
    # Note all are in kN/m
    selfWeight = (Depth/1000) * 25 * 1 
    floorFinish = 0.8 
    global factoredLoad
    factoredLoad = ( liveLoad + floorFinish + selfWeight ) * 1.5 
    print (f"Factored Load = {factoredLoad} kN/m")
    print("\n")

# Moment Calculation 
def Factored_Monent():
    print (f"Refer Table No 27 or 26 from IS-456:2000 Page no. 91")
    print (f"Enter ax and ay values corresponding to {lybylx}")
    ax = float(input("Enter the ax = "))
    ay = float(input("Enter the ay = "))
    global mux
    global muy
    mux = ax * factoredLoad * lx * lx 
    print(f"mux = {mux} kN-m")
    muy = ay * factoredLoad * lx * lx 
    print(f"muy={muy} kn-m ")
    global mu
    if (mux>muy):
        mu=mux
    else:
        mu=muy
    print("\n")

# Check for depth 
def Check_depth():
    global dmin
    if (gradeSteel==250):
        dmin = math.sqrt(mu*math.pow(10,6)/(0.148*gradeConcrete*1000))
    elif (gradeSteel==415):
        dmin = math.sqrt(mu*math.pow(10,6)/(0.138*gradeConcrete*1000))
    else :
        dmin = math.sqrt(mu*math.pow(10,6)/(0.133*gradeConcrete*1000))
    global safeD
    print(f"Depth Min = {dmin} mm")
    if(effectiveDepth>=dmin):
        safeD = "Depth is safe"
        print("Depth is safe")
    else:
        safeD = "Change the depth"
        print("Change the depth")
    print("\n")

# Reinforcement Calculations - Check with minmum ast missing 
def Reinforcemt_Calculation():
    wlx = 0.75 * ly
    wly = 0.75 * lx 
    # Reinforcement Along shorter span 
    temp1 = 1 - ((4.6*mux*math.pow(10,6))/(gradeConcrete*1000*math.pow(effectiveDepth,2)))
    pt = 50*(gradeConcrete/gradeSteel)*(1-math.sqrt(temp1))
    print(f"pt={pt}")
    CalAst =( pt/100 ) * 1000 * effectiveDepth
    global barAst
    global SSSpacing
    barAst = (math.pi/4)*math.pow(barDia,2)
    CalSpacing = (barAst/CalAst)*1000
    print(f"Calculated Spacing = {CalSpacing}")
    SSSpacing = float(input("Enter the Spacing in mm = "))
    astProvSS = (barAst/SSSpacing)*1000
    global minAst
    minAst = (0.12/100)*1000*Depth
    if(astProvSS<minAst):
        CalAst = minAst
        CalSpacing = (barAst/CalAst)*1000
        print(f"Calculated Spacing = {CalSpacing}")
        SSSpacing = float(input("Enter the Spacing in mm = "))
    print("\n")

    # Reinforcement along Longer span 
    global LSSpacing
    temp2 = 1 - ((4.6*muy*math.pow(10,6))/(gradeConcrete*1000*math.pow(effectiveDepth,2)))
    pty = 50*(gradeConcrete/gradeSteel)*(1-math.sqrt(temp2))
    print(f"pty={pty}")
    CalAstLS =( pty/100 ) * 1000 * effectiveDepth
    barAst = (math.pi/4)*math.pow(barDia,2)
    CalSpacingLS = (barAst/CalAstLS)*1000
    print(f"Calculated Spacing = {CalSpacingLS}")
    LSSpacing = float(input("Enter the Spacing in mm = "))
    astProvLS = (barAst/LSSpacing)*1000
    minAst = (0.12/100)*1000*Depth
    if(astProvLS<minAst):
        CalAstLS = minAst
        CalSpacingLS = (barAst/CalAstLS)*1000
        print(f"Calculated Spacing = {CalSpacingLS}")
        LSSpacing = float(input("Enter the Spacing in mm = "))  
    print("\n") 

    # Reinforcement in edge strips 
    global res
    res = (minAst/barAst)
    print(f"Calculated Reinforcement = {res}")
    res = float(input("Enter the round off res = "))
    print(f"Provide {res} Number of bars in the edge strips on both the directions")
    print("\n")

    # Torsional Reinforcemnt 
    tr = 0.75 * CalAst
    nr = (tr/barAst)
    print(f"Calculated No of Bars = {nr}")
    nr = float(input("Enter the round off no fo bars = "))
    global lxr
    global lyr
    lxr = lx / nr 
    lyr = ly / nr 
    print(lxr)
    print(lyr)

# Write to a file 
def Write_File():
    # f = open(input("File:"), "x")
    f = open(input("File:"), "w")
    f.write(f"Length of slab = {length} m \n")
    f.write(f"Breadth of slab = {breadth} m \n")
    f.write(f"Grade of Concrete = {gradeConcrete} n/mm2\n")
    f.write(f"Grade of Steel = {gradeSteel} n/mm2\n")    
    f.write(f"Live Load = {liveLoad} kN/m2\n")    
    f.write(f"Clear cover = {clearCover} mm \n")    
    f.write(f"Bar Diameter = {barDia} mm \n")  
    f.write("\n")  
    f.write(f"ly/lx = {lybylx}\n")    
    f.write(f"type of Slab = {typeSlab}\n")     
    f.write("\n")    
    f.write(f"Effecttive Depth = {effectiveDepth} mm \n")    
    f.write(f"Depth = {Depth} mm \n")       
    f.write("\n")  
    f.write(f"eff span x =lx = {lx} m\n")    
    f.write(f"eff span y =ly = {ly} m\n")    
    f.write("\n")  
    f.write(f"Factored Load = {factoredLoad} kN/m\n")   
    f.write("\n")   
    f.write(f"Moment Along shorter span = {mux} kN-m\n")    
    f.write(f"Moment Along longer span = {muy} kN-m \n")    
    f.write("\n")  
    f.write(f"d minimun = {dmin}\n")    
    f.write(f"{safeD}\n")    
    f.write("\n")  
    f.write(f"bar dia for all the reinforcement is = {barDia} mm \n")
    f.write(f"Shorter Span Spacing = {SSSpacing} mm\n")    
    f.write(f"Longer Span Spacing = {LSSpacing} mm \n")    
    f.write(f"Provide {res} Number of bars in the edge strips on both the directions \n")    
    f.write(f"Torsional Reingorcement distance along lx = {lxr * 1000} mm and ly = {lyr*1000} mm \n")    
    f.write(f"Programm Developed by PAVAN RAJ K \n")    

Check_Slab()
Effective_Depth() 
Effective_Span()  
Load_Calculation()
Factored_Monent()
Check_depth()
Reinforcemt_Calculation()
Write_File()

