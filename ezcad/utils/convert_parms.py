# -*- coding: utf-8 -*-
# Copyright (c) Ezcad Development Team. All Rights Reserved.
"""
Convert parameter dictionaries of cube.
"""

import os
from math import sqrt
import numpy as np
from ezcad.utils.convert_grid import get_step, xy2ln, ln2xy


def get_sgmt_from_parm(dict_parm, p1ilno=0, p1xlno=0, ilstep=12.5, xlstep=12.5):
    """
    Convert parm to sgmt. Default P1_ILNO and P1_XLNO are both zero.
    Default IL/XL step length is 12.5 meters. From the grids and
    coordinates in parm, sgmt can be derived.
    - dict_parm : dictionary, from reading parm file
    - p1ilno : integer, P1_ILNO (default 0)
    - p1xlno : integer, P1_XLNO (default 0)
    - ilstep : float, step length of IL (default 12.5m)
    - xlstep : float, step length of XL (default 12.5m)
    Return sgmt dictionary
    """
    p1crsx = dict_parm['TRACE_START']
    p1crsy = dict_parm['PANEL_START']
    dict_sgmt = {
        'P1_ILNO': p1ilno,
        'P1_XLNO': p1xlno,
        'P1_CRSX': p1crsx,
        'P1_CRSY': p1crsy
    }

    # In parm, TRACE is XL
    NTRACE = dict_parm['NTRACE']
    TRDX = dict_parm['TRDX']
    TRDY = dict_parm['TRDY']
    # In sgmt, P2 is end of first inline.
    # In other word, line P1-P2 represents the XL axis.
    lenx = TRDX * (NTRACE-1)
    leny = TRDY * (NTRACE-1)
    lengthAxisXL = sqrt(lenx**2 + leny**2)
    stepsXL = int(lengthAxisXL / xlstep)
    p2ilno = p1ilno
    p2xlno = p1xlno + stepsXL
    p2crsx = p1crsx + lenx
    p2crsy = p1crsy + leny
    dict_sgmt['P2_ILNO'] = p2ilno
    dict_sgmt['P2_XLNO'] = p2xlno
    dict_sgmt['P2_CRSX'] = p2crsx
    dict_sgmt['P2_CRSY'] = p2crsy

    # In parm, PANEL is IL
    NPANEL = dict_parm['NPANEL']
    PNDX = dict_parm['PNDX']
    PNDY = dict_parm['PNDY']
    # In sgmt, P3 is end of first crossline.
    # In other word, line P1-P3 represents the IL axis.
    lenx = PNDX * (NPANEL-1)
    leny = PNDY * (NPANEL-1)
    lengthAxisIL = sqrt(lenx**2 + leny**2)
    stepsIL = int(lengthAxisIL / ilstep)
    p3ilno = p1ilno + stepsIL
    p3xlno = p1xlno
    p3crsx = p1crsx + lenx
    p3crsy = p1crsy + leny
    dict_sgmt['P3_ILNO'] = p3ilno
    dict_sgmt['P3_XLNO'] = p3xlno
    dict_sgmt['P3_CRSX'] = p3crsx
    dict_sgmt['P3_CRSY'] = p3crsy
    return dict_sgmt


def get_vxyz_from_vidx(dict_vidx, survey):
    IL_FRST = dict_vidx['IL_FRST']
    XL_FRST = dict_vidx['XL_FRST']
    XL_LAST = dict_vidx['XL_LAST']
    IL_LAST = dict_vidx['IL_LAST']
    points_ln = np.array([[IL_FRST, XL_FRST],
                          [IL_FRST, XL_LAST],
                          [IL_LAST, XL_FRST]])
    points_xy = ln2xy(points_ln, survey=survey)

    AXIS_ORX, AXIS_ORY = points_xy[0]
    AXIS_XLX, AXIS_XLY = points_xy[1]
    AXIS_ILX, AXIS_ILY = points_xy[2]
    AXIS_DPX, AXIS_DPY = AXIS_ORX, AXIS_ORY

    AXIS_ORZ = dict_vidx['DP_FRST']
    AXIS_XLZ = AXIS_ORZ
    AXIS_ILZ = AXIS_ORZ

    SAMPLE_INC = dict_vidx['DP_NCRT']
    NSAMPLE = dict_vidx['DP_AMNT']
    AXIS_DPZ = AXIS_ORZ + SAMPLE_INC * (NSAMPLE-1)

    dict_vxyz = {
        'AXIS_ORX': AXIS_ORX,
        'AXIS_ORY': AXIS_ORY,
        'AXIS_ORZ': AXIS_ORZ,
        'AXIS_DPX': AXIS_DPX,
        'AXIS_DPY': AXIS_DPY,
        'AXIS_DPZ': AXIS_DPZ,
        'AXIS_XLX': AXIS_XLX,
        'AXIS_XLY': AXIS_XLY,
        'AXIS_XLZ': AXIS_XLZ,
        'AXIS_ILX': AXIS_ILX,
        'AXIS_ILY': AXIS_ILY,
        'AXIS_ILZ': AXIS_ILZ
    }
    return dict_vxyz


def get_parm_from_vidx(dict_vidx, survey, **kwargs):
    """
    -i- dict_vidx : dictionary, volume indexes
    -i- survey : Survey
    -i- kwargs : keyword arguments
        dataPrecision : integer, 4 for 32-bit float, 8 for 64-bit float.
        dataVelType : string, 'AVGVEL', 'INTVEL', 'RMSVEL'
        depthOutput : string, 'POSITIVE', 'NEGATIVE'
        traceUnit : string, 'METERS', 'FEET'
        panelUnit : string, 'METERS', 'FEET'
        sampleUnit : string, 'MSECS', 'METERS', 'FEET'
        dataUnit : string, 'METERSPERSEC', 'FEETPERSEC'
    -o- dict_parm : dictionary, VTB binary cube parameters
    Convert vidx to parm
    """
    dict_parm = {} # initialize

    # get IL/XL unit step vector
    ILDX, ILDY = survey.step['iline']
    XLDX, XLDY = survey.step['xline']
    TRDX = XLDX * dict_vidx['XL_NCRT']
    TRDY = XLDY * dict_vidx['XL_NCRT']
    PNDX = ILDX * dict_vidx['IL_NCRT']
    PNDY = ILDY * dict_vidx['IL_NCRT']
    dict_parm['TRDX'] = TRDX
    dict_parm['TRDY'] = TRDY
    dict_parm['PNDX'] = PNDX
    dict_parm['PNDY'] = PNDY

    dict_parm['NTRACE'] = dict_vidx['XL_AMNT']
    dict_parm['NPANEL'] = dict_vidx['IL_AMNT']
    dict_parm['NSAMPLE'] = dict_vidx['DP_AMNT']

    IL_FRST = dict_vidx['IL_FRST']
    XL_FRST = dict_vidx['XL_FRST']
    origin_ln = np.array([IL_FRST, XL_FRST])
    origin_xy = ln2xy(origin_ln, survey=survey)
    dict_parm['TRACE_START'] = origin_xy[0]
    dict_parm['PANEL_START'] = origin_xy[1]
    dict_parm['SAMPLE_START'] = dict_vidx['DP_FRST']
    dict_parm['TRACE_INC'] = sqrt(TRDX**2 + TRDY**2)
    dict_parm['PANEL_INC'] = sqrt(PNDX**2 + PNDY**2)
    dict_parm['SAMPLE_INC'] = dict_vidx['DP_NCRT']
    # Following entries come from keyword arguments
    dataPrecision = kwargs.get('dataPrecision', 4)
    dataVelType = kwargs.get('dataVelType', 'amplitude')
    depthOutput = kwargs.get('depthOutput', 'POSITIVE')
    traceUnit = kwargs.get('traceUnit', 'METERS')
    panelUnit = kwargs.get('panelUnit', 'METERS')
    sampleUnit = kwargs.get('sampleUnit', 'MSECS')
    dataUnit = kwargs.get('dataUnit', 'METERSPERSEC')
    dict_parm['DATA_PRECISION'] = dataPrecision
    dict_parm['DATA_VEL_TYPE'] = dataVelType
    dict_parm['DEPTH_OUTPUT'] = depthOutput
    dict_parm['TRACE_UNIT'] = traceUnit
    dict_parm['PANEL_UNIT'] = panelUnit
    dict_parm['SAMPLE_UNIT'] = sampleUnit
    dict_parm['DATA_UNIT'] = dataUnit
    # dict_parm['DATA_MIN'] = 1500
    # dict_parm['DATA_MAX'] = 6000

    return dict_parm


def get_vidx_from_parm(dict_parm, dict_sgmt):
    """
    Convert parm to vidx (volume index)
    - dict_parm : dictionary, from reading parm file
    - dict_sgmt : dictionary, from reading sgmt file
    Return vidx dictionary
    """
    DP_FRST = dict_parm['SAMPLE_START']
    DP_NCRT = dict_parm['SAMPLE_INC']
    DP_AMNT = dict_parm['NSAMPLE']
    DP_LAST = DP_FRST + DP_NCRT * (DP_AMNT-1)

    XL_AMNT = dict_parm['NTRACE']
    IL_AMNT = dict_parm['NPANEL']

    OX = dict_parm['TRACE_START']
    OY = dict_parm['PANEL_START']
    origin_xy = np.array([OX, OY])
    IL_FRST, XL_FRST = xy2ln(origin_xy, dict_sgmt)

    # get IL/XL unit step vector
    ILDX, ILDY, XLDX, XLDY = get_step(dict_sgmt)

    # In parm, TRACE is XL
    if XLDX != 0:
        TRDX = dict_parm['TRDX']
        XL_NCRT = int(round(TRDX/XLDX))
    elif XLDY != 0:
        TRDY = dict_parm['TRDY']
        XL_NCRT = int(round(TRDY/XLDY))
    else:
        raise ValueError("Both XLDX and XLDY are zero.")
    XL_LAST = XL_FRST + XL_NCRT * (XL_AMNT-1)

    # In parm, PANEL is IL
    if ILDX != 0:
        PNDX = dict_parm['PNDX']
        IL_NCRT = int(round(PNDX/ILDX))
    elif ILDY != 0:
        PNDY = dict_parm['PNDY']
        IL_NCRT = int(round(PNDY/ILDY))
    else:
        raise ValueError("Both ILDX and ILDY are zero.")
    IL_LAST = IL_FRST + IL_NCRT * (IL_AMNT-1)

    dict_vidx = {
        'IL_FRST': int(IL_FRST),
        'IL_LAST': int(IL_LAST),
        'IL_NCRT': int(IL_NCRT),
        'IL_AMNT': int(IL_AMNT),
        'XL_FRST': int(XL_FRST),
        'XL_LAST': int(XL_LAST),
        'XL_NCRT': int(XL_NCRT),
        'XL_AMNT': int(XL_AMNT),
        'DP_FRST': int(DP_FRST),
        'DP_LAST': int(DP_LAST),
        'DP_NCRT': int(DP_NCRT),
        'DP_AMNT': int(DP_AMNT)
    }
    return dict_vidx


def get_vxyz_from_parm(dict_parm):
    """
    Convert parm to vxyz (volume corners xyz)
    - dict_parm : dictionary, from reading parm file
    Return vxyz dictionary
    """
    AXIS_ORX = dict_parm['TRACE_START']
    AXIS_ORY = dict_parm['PANEL_START']
    AXIS_ORZ = dict_parm['SAMPLE_START']

    NSAMPLE = dict_parm['NSAMPLE']
    SAMPLE_INC = dict_parm['SAMPLE_INC']
    AXIS_DPX = AXIS_ORX
    AXIS_DPY = AXIS_ORY
    AXIS_DPZ = AXIS_ORZ + SAMPLE_INC * (NSAMPLE-1)

    # In parm, TRACE is XL
    NTRACE = dict_parm['NTRACE']
    TRDX = dict_parm['TRDX']
    TRDY = dict_parm['TRDY']
    AXIS_XLX = AXIS_ORX + TRDX * (NTRACE-1)
    AXIS_XLY = AXIS_ORY + TRDY * (NTRACE-1)
    AXIS_XLZ = AXIS_ORZ

    # In parm, PANEL is IL
    NPANEL = dict_parm['NPANEL']
    PNDX = dict_parm['PNDX']
    PNDY = dict_parm['PNDY']
    AXIS_ILX = AXIS_ORX + PNDX * (NPANEL-1)
    AXIS_ILY = AXIS_ORY + PNDY * (NPANEL-1)
    AXIS_ILZ = AXIS_ORZ

    dict_vxyz = {
        'AXIS_ORX': AXIS_ORX,
        'AXIS_ORY': AXIS_ORY,
        'AXIS_ORZ': AXIS_ORZ,
        'AXIS_DPX': AXIS_DPX,
        'AXIS_DPY': AXIS_DPY,
        'AXIS_DPZ': AXIS_DPZ,
        'AXIS_XLX': AXIS_XLX,
        'AXIS_XLY': AXIS_XLY,
        'AXIS_XLZ': AXIS_XLZ,
        'AXIS_ILX': AXIS_ILX,
        'AXIS_ILY': AXIS_ILY,
        'AXIS_ILZ': AXIS_ILZ
    }
    return dict_vxyz


def main():
    pass
    # from ezcad.utils.print_dict import print_vidx, print_vxyz, \
    #     print_parm, print_sgmt
    # from ezcad.gosurvey.impt.read_file import read_sgmt
    # from ezcad.gocube.expt.write_file import write_vidx, write_vxyz
    # sgmtfn = "/home/zhu/block9_survey_geometry.sgmt"
    # parmfn = "/data/Dropbox/test/vm_time_vint.parm"
    # read parm file to dictionary
    # from ezcad.utils.vtb_seis import read_parm
    # dict_parm = read_parm(parmfn)
    # print_parm(dict_parm)
    # convert parm to vxyz and write file
    # dict_vxyz = get_vxyz_from_parm(dict_parm)
    # print_vxyz(dict_vxyz)
    # fpre = os.path.splitext(parmfn)[0]
    # vxyzfn = fpre + ".vxyz"
    # write_vxyz(vxyzfn, dict_vxyz)
    # read sgmt file to dictionary
    # dict_sgmt = read_sgmt(sgmtfn)
    # print_sgmt(dict_sgmt)
    # calculate vidx and write file
    # dict_vidx = get_vidx_from_parm(dict_parm, dict_sgmt)
    # print_vidx(dict_vidx)
    # vidxfn = fpre + ".vidx"
    # write_vidx(vidxfn, dict_vidx)


if __name__ == '__main__':
    main()
