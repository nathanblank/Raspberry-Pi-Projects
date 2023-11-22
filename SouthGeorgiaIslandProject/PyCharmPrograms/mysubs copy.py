import numpy as np  #instead of writing "numpy." just use "np."
import matplotlib.pyplot as plt

#import pandas as pd
from optparse import OptionParser

# reads a file of landmask map (uint8(nlats, nlons), latitude values (float32(nlats)), and lon values (float32(nlons))
# written by ETOP05landmask_2.py
# uses np.memmap with 3 separate reads, 1 for each array
# call would be: LM_arr, LAT_arr, LON_arr = rd_landmask(landmaks_dist, nlats (typ. 2160), nlons (typ. 4320)
def rd_landmask(landmask_dist, nlats, nlons):
    # construct file name for existing landmask file
    infile = "./LANDMASK_%d_NLATS_%d_NLONS_%d_.bytemap" % (landmask_dist, nlats, nlons)
    landmask_arr = np.memmap(infile, mode='r', dtype='uint8', shape=(nlats, nlons))  # read landmask byte array, no offset
    # now read the latitude array (float32, nlats long)  -- requires an offset
    off1 = nlats * nlons   # number of bytes in the landmask array on the disk
    rlats_arr = np.memmap(infile, mode='r', dtype='float32', shape=(nlats), offset=off1)
    off2 = off1 + (nlats * 4)  # offset for the landmask+rlats_arr arrays on the disk, in bytes from start of file
    rlons_arr = np.memmap(infile, mode='r', dtype='float32', shape=(nlons), offset=off2)
    return landmask_arr, rlats_arr, rlons_arr

def rd_reverse_landmask(landmask_dist, nlats, nlons):
    # construct file name for existing landmask file
    infile = "./LANDMASK_%d_NLATS_%d_NLONS_%d_.reverse_bytemap" % (landmask_dist, nlats, nlons)
    landmask_arr = np.memmap(infile, mode='r', dtype='uint8', shape=(nlats, nlons))  # read landmask byte array, no offset
    # now read the latitude array (float32, nlats long)  -- requires an offset
    off1 = nlats * nlons   # number of bytes in the landmask array on the disk
    rlats_arr = np.memmap(infile, mode='r', dtype='float32', shape=(nlats), offset=off1)
    off2 = off1 + (nlats * 4)  # offset for the landmask+rlats_arr arrays on the disk, in bytes from start of file
    rlons_arr = np.memmap(infile, mode='r', dtype='float32', shape=(nlons), offset=off2)
    return landmask_arr, rlats_arr, rlons_arr

# testBit() returns a nonzero result, 2**offset, if the bit at 'offset' is one.

def testBit(int_type, offset):
    mask = 1 << offset
    return(int_type & mask)

# setBit() returns an integer with the bit at 'offset' set to 1.

def setBit(int_type, offset):
    mask = 1 << offset
    return(int_type | mask)

# clearBit() returns an integer with the bit at 'offset' cleared.

def clearBit(int_type, offset):
    mask = ~(1 << offset)
    return(int_type & mask)

# toggleBit() returns an integer with the bit at 'offset' inverted, 0 -> 1 and 1 -> 0.

def toggleBit(int_type, offset):
    mask = 1 << offset
    return(int_type ^ mask)


# function to print out bit representation of a number (from the web)
# A is input list or array
# grp is input grouping of bits
#run
##  A = [0,1,2,127,128,255]
##  bprint (A,4)
def bprint(A, grp):
    for x in A:
        brp = "{:16b}".format(x)
        L=[]
        for i,b in enumerate(brp):
            if b=="1":
                L.append("1")
            else:
                L.append("0")
            if (i+1)%grp ==0 :
                L.append(" ")

        print("".join(L))


# getLM returns a 0 if LAND, and 1 if not-land
# Note that this is opposite to the convention in the landmask array (where 1 = land)
# landmask array is provided as an input to the procedure, along with (real) wvc_lat and (real) wvc_lon
def getLM(lm_array, wvc_lat, wvc_lon):
    flip = [1,0]  # array to flip landmask values from 0 to 1 and vice versa - could also do this with "toggle"
    ilat = int((90.-wvc_lat)*12.)  # entry into the lm_array, which has 0 index = 90 degrees; no rounding
    ilon = int(wvc_lon*12.)  # same for longitude - no rounding

    val = lm_array[ilat, ilon]  # raw value from the input landmask array (1 = LAND)
    outval = flip[val]
    return(outval)

def getLM_vector(lm_array, wvc_lat, wvc_lon):
    # function to actually return a boolean array (3248, 152) array of landmask values given input landmask,
    #  and indices into the landmask array provided by getLM_indices_vector
    # output value of 0 (false) indicates LAND
    flip = [1,0]  # array to flip landmask values from 0 to 1 and vice versa - could also do this with "toggle"
    ilat = int((90.-wvc_lat)*12.)  # entry into the lm_array, which has 0 index = 90 degrees; no rounding
    ilon = int(wvc_lon*12.)  # same for longitude - no rounding

    val = lm_array[ilat, ilon]  # raw value from the input landmask array (1 = LAND)
    outval = flip[val]
    return(outval)

#def getLM_indices_vector(wvc_lat, wvc_lon):
#    #  yields UNROUNDED indices into the ETOPO5 landmask array with inputs the wvc_lat and wvc_lon row, wvc ARRAYS
#    # call is -   wvc_lat_ind, wvc_lon_ind = getLM_indices(wvc_lat, wvc_lon)
#    scl = 90.*12.
#    wvc_lat_ind = wvc_lat.copy()
#    wvc_lon_ind = wvc_lon.copy()
#    wvc_lat_ind *= 12.  # efficient multiplication of array
#    wvc_lat_ind = np.int(scl - wvc_lat_ind)
#    wvc_lon_ind *= 12.
#    wvc_lon_ind = np.int(wvc_lon_ind)
#    return, wvc_lat_ind, wvc_lon_ind


#    90.-wvc_lat_ind = int((90.-wvc_lat)*12.)  # entry into the lm_array, which has 0 index = 90 degrees; no rounding
#    ilon = int(wvc_lon*12.)  # same for longitude - no rounding

#    val = lm_array[ilat, ilon]  # raw value from the input landmask array (1 = LAND)
#    outval = flip[val]
#    return wvc_lat_ind, wvc_lon_ind


#-----

# getmyflag returns a value of 1 IF THE WVC FLAGS INDICATE A GOOD RETRIEVAL (opposite to basic sense of the flag
#    in the data
# this function IGNORES:  high-wind speed flags, azimuth diversity flag, 4-looks flag
# input argument is the raw flag from the qscat v3.1 wvc
def myflag(in_flag):
    tmp = in_flag
    # clear the high-wind speed bit, etc
    tmp = ms.clearBit(tmp, 10)  # high wind speed
    tmp = ms.clearBit(tmp, 14)  # all 4 looks

    tmp1 = (1 if tmp == 0 else 0)  ###THIS IS AN IF STATEMENT
    return(tmp1)

def flightang2(nrows):

    #Function to return the approximate flight angle (in degrees from North) at each
    #orbit step (nrows steps/orbit) for QSCAT, given an approximate
    #orbit inclination of 98.6 degrees.

    #Output is a floating point array object of length 1624

    #From Scott Dunbar (original code is an IDL pro)

    import numpy as np
    import matplotlib.pyplot as plt

    #print('IN FLIGHTANG2')

    wi = np.linspace(start=0., stop=nrows, num=nrows, dtype=float)
    u = wi*(360./nrows) - 90.
    cosu = np.cos(np.radians(u))
    inc = np.radians(98.6)  # orbit inclination - hardwired
    tani = np.tan(inc)
    arg = 1./(cosu*tani)
    ang = np.rad2deg(np.arctan(arg))
    #plt.plot(ang)

    desc_start = np.uint(nrows / 2)

    tmp = ang[desc_start:]
    tmp = -(180. - tmp)
    ang[desc_start:] = tmp

    #plt.plot(ang)
    #print('start of descent step(row):  ', desc_start)

    return ang

# inputs # ambiguities, and a 2, 1-D array (nambigs) of spd, dir (in degrees)
# outputs 2-d array of x, y landmarks such that x = -spd*sin(dir), y = spd*cos(dir)
def gen_landmarks(in_spd, in_dir):
    # get nambigs from the size of the input arrays
    nambigs = np.shape(in_spd)[0]
    spds = in_spd
    angs = np.deg2rad(in_dir)  # make into radians

    landmarks_arr = np.zeros((nambigs, 2), dtype=np.float32)  # column 0 will be x, 1 will be y
    landmarks_arr[:, 0] = -in_spd*np.sin(angs)
    landmarks_arr[:, 1] = in_spd*np.cos(angs)

    return landmarks_arr

def comp_landmarks(soln1, soln2):
    # a func to plot ambiguities-as-landmarks from 2 input solutions
    # the # of ambiguitie is taken from the shape of the input arrays

    nambigs = soln1.shape[0]

    x1 = soln1[:, 0]  # xvals for solution 1
    x2 = soln2[:, 0]
    y1 = soln1[:, 1]
    y2 = soln2[:, 1]

    maxx = max(abs(np.amax(x1)), abs(np.amax(x2)))
    maxy = max(abs(np.amax(y1)), abs(np.amax(y2)))
    maxlim = max(maxx, maxy) + 1   # set the symmetric limit for the plot axes

    fig_x = plt.figure(figsize=(4, 4))  # make it square and symmetric

    plt.xlim([-maxlim-1, maxlim])
    plt.ylim([-maxlim-1, maxlim])

    for j in range(0, nambigs):
        plt.plot([0., x1[j]], [0., y1[j]], 'ko-')  # solution 1 will be black
        plt.plot([0., x2[j]], [0., y2[j]], 'ro-')  # solution 2 will be red

        plt.show()


def F(C):
    return (9.0/5)*C + 32

def F2(C):
    C2 = 2.*C
    C1 = (9.0/5)*C + 32
    return C1, C2

def F3(C):
    C3 = 3*C
    C2 = 2*C
    C1 = C
    return C1, C2, C3
