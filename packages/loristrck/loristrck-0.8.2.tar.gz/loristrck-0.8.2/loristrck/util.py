import os
import numpy as np
import numpyx as npx
import logging


from . import _core

try: 
    from typing import List, Tuple
except ImportError:
    pass


logger = logging.getLogger("loristrck")


def concat(partials, fade=0.005, edgefade=0):   
    """
    Concatenate multiple Partials to produce a new one.
    Assumes that the partials are non-overlapping and sorted

    partials: a seq. of partials (each partial is a 2D-array)
    fade: fadetime to apply at the end/beginning of each concatenated partial
    edgefade: a fade to apply at the beginning of the first and at
              the end of the last partial

    partials need to be non-simultaneous and sorted
    """
    # fade = max(fade, 128/48000.)
    numpartials = len(partials)
    if numpartials == 0:
        raise ValueError("No partials to concatenate")
    T, F, A, B = [], [], [], []
    eps = 0.000001
    fade0 = fade
    fade = fade - 2*eps
    zeros4 = np.zeros((4,), dtype=float)
    zeros1 = np.zeros((1,), dtype=float)

    if edgefade > 0:
        p = partials[0]
        t0 = p[0, 0] - edgefade
        if t0 > 0:
            T.append([t0])
            F.append([p[0, 1]])
            A.append([0])
            B.append([0])
    
    if numpartials == 1:
        p = partials[0]
        T.append(p[:,0])
        F.append(p[:,1])
        A.append(p[:,2])
        B.append(p[:,4])
    else:
        for i in range(len(partials) - 1):
            p0 = partials[i]
            p1 = partials[i+1]
            if p1[0, 0] - p0[-1, 0] < fade0*2:
                raise ValueError("Partials overlap, can't concatenate")
            T.append(p0[:,0])
            F.append(p0[:,1])
            A.append(p0[:,2])
            B.append(p0[:,4])
            if fade > 0:
                f0 = p0[-1, 1]
                f1 = p1[0, 1]
                t0 = p0[-1, 0]
                t1 = p1[0, 0]
                tmid = (t0+t1)*0.5
                T.append([t0+fade, tmid-eps, tmid+eps, t1-fade])
                F.append([f0,      f0,       f1,       f1])
                A.append(zeros4)
                B.append(zeros4)
        T.append(p1[:,0])
        F.append(p1[:,1])
        A.append(p1[:,2]) 
        B.append(p1[:,4])
    
    p = partials[-1]
    if p[-1, 2] > 0 and edgefade > 0:
        t1 = p[-1, 0]
        f1 = p[-1, 1]
        T.append([t1 + edgefade])
        F.append([f1])
        A.append(zeros1)
        B.append(zeros1)
    
    times = np.concatenate(T)
    freqs = np.concatenate(F)
    amps = np.concatenate(A)
    bws = np.concatenate(B)
    phases = np.zeros_like(bws)
    return np.column_stack((times, freqs, amps, phases, bws))


def _get_best_track(tracks, partial, gap, acceptabledist):
    """
    Get the best track minimizing gap
    """
    pt0 = partial[0, 0]
    mindist = float("inf")
    best = None
    for track in tracks:
        t1 = track[-1][-1, 0] + gap
        if t1 < pt0:
            dist = t1 - pt0
            if dist < acceptabledist:
                return track
            if dist < mindist:
                best = track
                mindist = dist
    return best


def _join_track(partials, fade):
    assert fade > 0
    p = concat(partials, fade=fade, edgefade=fade)
    # assert npx.array_is_sorted(p[:,0])
    if p[0, 0] > 0:
        assert p[0, 2] == 0
    assert p[-1, 2] == 0
    return p


def pack(partials, numtracks=0, gap=0.010, fade=-1, acceptabledist=0.100):
    """
    Pack non-simultenous partials into longer partials with
    silences in between. These packed partials can be used
    as tracks for resynthesis, minimizing the need
    of oscillators. 

    partials: 
        a list of arrays, where each array represents a partial, 
        as returned by analyze
    
    numtracks: 
        if > 0, sets the maximum number of tracks. Partials not 
        fitting in will be discarded

    gap: 
        minimum gap between partials in a track. Should be longer than 
        2 times the sampling interval, if the packed partials are later 
        going to be resampled.

    fade: 
        apply a fade to the partials before joining them. 
        If not given, a default value is calculated

    acceptabledist: 
        instead of searching for the best possible fit, pack two partials 
        together if they are near enough

    RETURNS: the packed partials (a list of numpy arrays)

    NB: amplitude is always faded out between partials

    See also: partials_save_matrix
    """

    tracks = []
    mingap = 0.010
    if gap < mingap:
        gap = mingap
        logger.info(f"pack: gap value is too small. Using default: {gap}")
    if fade < 0:
        fade = min(0.005, gap / 3.0)
        logger.debug(f"pack: using fade={fade}")
    clearance = gap + 2*fade
    
    for partial in partials:
        best_track = _get_best_track(tracks, partial, clearance, acceptabledist)
        if best_track is not None:
            best_track.append(partial)
        else:
            if numtracks == 0 or len(tracks) < numtracks:
                track = [partial]
                tracks.append(track)

    partials = [_join_track(track, fade=fade) for track in tracks]
    return partials


def partial_sample_regularly(p, dt, t0=-1, t1=-1):
    # type: (np.ndarray, float, float, float) -> np.ndarray
    """
    Sample a partial `p` at regular time intervals

    p: a partial represented as a 2D-array with columns
       times, freqs, amps, phases, bws
    dt: sampling period
    t0, t1: start and end times, or -1 to use the start and
            end times of the partial
    
    Returns a partial (2D-array with columns times, freqs, amps, phases, bws)
    """
    if t0 < 0:
        t0 = p[0, 0]
    if t1 <= 0:
        t1 = p[-1, 0]
    times = np.arange(t0, t1+dt, t1)
    return partial_sample_at(p, times)


def partial_sample_at(p, times):
    # type: (np.ndarray, np.ndarray) -> np.ndarray
    """
    Sample a partial `p` at given times

    p: a partial represented as a 2D-array with columns
       times, freqs, amps, phases, bws

    Returns a partial (2D-array with columns times, freqs, amps, phases, bws)
    """
    times = np.asarray(times, dtype=float)
    data = npx.table_interpol_linear(p, times)
    timescol = times.reshape((times.shape[0], 1))
    resampled = np.hstack((timescol, data))
    return resampled


def partial_crop(p, t0, t1):
    # type: (np.ndarray, float, float) -> np.ndarray
    """
    Crop partial at times t0, t1

    * Returns p if p is included in the interval t0-t1
    * Returns None if partial is not defined between t0-t1
    * Otherwise crops the partial at t0 and t1, places a breakpoint
      at that time with the interpolated value
    """
    times = p[:,0] 
    pt0 = times[0]
    pt1 = times[-1]
    if pt0 > t0 and pt1 < t1:
        return p
    if t0 > pt1 or t1 < pt0:
        return None
    idxs = times > t0 
    idxs *= times < t1
    databetween = p[idxs]
    arrays = []
    if t0 < databetween[0, 0] and t0 > pt0:
        arrays.append(partial_sample_at(p, [t0]))
    arrays.append(databetween)
    if t1 > databetween[-1, 0] and t1 < pt1:
        arrays.append(partial_sample_at(p, [t1]))
    return np.vstack(arrays)
    

def partials_sample(sp, dt=0.002, t0=-1, t1=-1, maxstreams=0, interleave=True):
    # type: (List[np.ndarray], float, float, float, bool) -> Any
    """
    Samples the partials between times `t0` and `t1` with a sampling
    period `dt`. 

    sp: a list of 2D-arrays, each representing a partial
    dt: sampling period
    t0: start time, or None to use the start time of the spectrum
    t1: end time, or None to use the end time of the spectrum
    interleave: if True, all columns of each partial are interleaved
                (see below)

    To be used in connection with `pack`, which packs short non-simultaneous 
    partials into longer ones. The result is a 2D matrix representing the partials.

    Sampling times is calculated as: times = arange(t0, t1+dt, dt)

    * If interleave is True, it returns a big matrix of format

    [[f0, amp0, bw0, f1, amp1, bw1, …, fN, ampN, bwN],   # times[0]
     [f0, amp0, bw0, f1, amp1, bw1, …, fN, ampN, bwN],   # times[1]
     ... 
    ]

    Where (f0, amp0, bw0) represent the freq, amplitude and bandwidth 
    of partial 0 at a given time, (f1, amp1, bw0) the corresponding data 
    for partial 1, etc.

    * If interleave is False, it returns three arrays: freqs, amps, bws
      of the form

    [[f0, f1, f2, ..., fn]  @ times[0]
     [f0, f1, f2, ..., fn]  @ times[1]
    ]
    
    See also
    ========

    * matrix_save
    * partials_save_matrix

    NB: phase information is not sampled
    """
    if t0 < 0:
        t0 = min(p[0, 0] for p in sp)
    if t1 <= 0:
        t1 = max(p[-1, 0] for p in sp)
    times = np.arange(t0, t1+dt, dt)
    if not interleave:
        freqs, amps, bws = [], [], []
        for p in sp:
            out = npx.table_interpol_linear(p, times)
            freqs.append(out[:,0])
            amps.append(out[:,1])
            bws.append(out[:,3])
        freqarray = np.column_stack(freqs)
        amparray = np.column_stack(amps)
        bwarray = np.column_stack(bws)
        if maxstreams > 0:
            _limit_matrix(amparray, maxstreams)
        return freqarray, amparray, bwarray
    else:
        cols = []
        for p in sp:
            p_resampled = npx.table_interpol_linear(p, times)
            # Extract columns: freq, amp, bw (freq is now index 0, because
            # the resampled partial has no times column)
            cols.append(p_resampled[:,(0, 1, 3)])
        m = np.hstack(cols)
        if maxstreams > 0:
            _limit_matrix_interleaved(m, maxstreams)
        return m


def _limit_matrix(m, maxstreams):
    for i in range(len(m)):
        amps = m[i]
        idxs = np.argsort(amps)[:-maxstreams]
        m[idxs] = 0


def _limit_matrix_interleaved(m, maxstreams):
    numrows = m.shape[0]
    for i in range(numrows):
        amps = m[i, 1::3]
        idxs = np.argsort(amps)[:-maxstreams]
        amps[idxs] = 0
            

def meanamp(partial):
    # type: (np.ndarray) -> float
    """
    Returns the mean amplitude of a partial

    partial: a numpy 2D-array representing a Partial
    """
    # todo: Use the times to perform an integration rather than
    # just returning the mean of the amps
    return _core.meancol(partial, 2)
    

def partial_energy(partial):
    # type: (np.ndarray) -> float
    """
    Integrate the partial amplitude over time. Serves as measurement
    for the energy contributed by the partial.
    """
    dur = partial[-1, 0] - partial[0, 0]
    return meanamp(partial) * dur


def _db2amp(x):
    # type: (float) -> float
    return 10.0 ** (0.05 * x)


def select(partials, mindur=0, minamp=-120, maxfreq=24000, minfreq=0, 
           minbps=1):
    # type: (List[np.ndarray], float, float, int, int, int) -> List[np.ndarray]
    """
    Selects a seq. of partials matching the given conditions

    * partials: a list of numpy 2D arrays, each array representing 
                a partial

    Select only those partials which have:
        * a min. duration of at least `mindur` AND
        * an avg. amplitude of at least `minamp` AND
        * a freq. between `minfreq` and `maxfreq` AND
        * have at least `minbps` breakpoints

    Returns 2 lists: (selected partials, unselected)

    Example: filter out noise

    partials = read_sdif(...)
    selected, _ = select(partials, minbps=2, mindur=0.005, minamp=-80, maxfreq=17000)
    """
    amp = _db2amp(minamp)
    selected = []
    unselected = []
    checkfreq = minfreq > 0 or maxfreq < 24000
    checkbps = minbps > 1 or mindur > 0
    for p in partials:
        if checkbps:
            if len(p) < minbps or p[-1, 0] - p[0, 0] < mindur:
                unselected.append(p)
                continue
        if checkfreq:
            f0, f1 = npx.minmax1d(p[:,1])
            if minfreq > f0 or f1 > maxfreq: 
                unselected.append(p)
                continue
        if minamp > -120:
            if meanamp(p) < amp:
                unselected.append(p)
                continue
        selected.append(p)
    return selected, unselected


def loudest(partials, N):
    # type: (List[np.ndarray], int) -> List[np.ndarray]
    """
    Get the loudest N partials

    The returned partials will be sorted by declining energy 
    (integrated amplitude)
    """
    return sorted(partials, key=partial_energy, reverse=True)[:N]
    

def matrix_save(m,             # type: np.ndarray 
                sndfile,       # type: str,
                dt,            # type: float,
                t0=0,          # type: float
                bits=32,       # type: int 
                header=True,   # type: bool
                metadata=True  # type: bool
                ):
    # type: (...) -> None
    """
    Save the raw data in m as a float32 soundfile. This is not a real 
    soundfile but it is used to transfer the data in binary form to be 
    read in another application. Supported formats are "wav" and "aiff". 
    The advantage of using a soundfile to transfer raw data is the 
    portability (no endianness problem) and the availability of fast
    libraries for many applications.

    m      : a 2D-matrix as returned by `partials_sample`
    sndfile: the path to the resulting soundfile (wav or aif)
    dt     : the sampling period used to sample the partials.
    t0     : the start time of the sampled partials
    bits   : 32 or 64. 32 bits should be enough
    header : if True, a header is included with the format
             [dataOffset, dt, numcols, numrows, t0]
    metadata: If True, metadata is included which duplicates the 
              data of the header in string form.    

    Each row corresponds to a sample of all partials, the time of 
    each row can be determined by

    times = arange(t0, t0+dt*numrows, dt)

    The data `m` is a 2D numpy array. It is written as a flat array after
    the header

    Example
    =======

    partials = read_sdif(path_to_sdif)
    # Eliminate very short-lived partials
    partials, _ = select(minbps=2, mindur=0.002)  
    tracks = pack(partials)
    dt = 64/44100
    m = partials_sample(tracks, dt)
    numrows, numcols = m.shape
    matrix_save(m, dt, "out.wav")
    
    Applications which can make use of this data include csound 
    (via its opcode adsynt2)

    See also: partials_save_matrix
    """
    import pysndfile
    ext = os.path.splitext(sndfile)[1][1:][:3].lower()
    assert ext in ('wav', 'aif')
    assert bits in (32, 64)
    encoding = "float%d" % bits
    fmt = pysndfile.construct_format(ext, encoding)
    f = pysndfile.PySndfile(sndfile, mode="w", format=fmt, channels=1, 
                            samplerate=44100)
    numrows, numcols = m.shape
    if metadata:
        metastr = b"DataStart=%d, SamplingPeriod=%f, NumCols=%d, NumRows=%d, TimeStart=%f" % \
                  (5, dt, numcols, numrows, t0)
        f.set_string("SF_STR_COMMENT", metastr)
        f.set_string("SF_STR_SOFTWARE", b"loristrck")
    if header:
        header_array = np.array([5, dt, numcols, numrows, t0], dtype=float)
        f.write_frames(header_array)
    mflat = m.ravel()
    f.write_frames(mflat)
    f.writeSync()


def partials_save_matrix(partials, dt, sndfile, gapfactor=3, maxstreams=0):
    # type: (List[np.ndarray], float, str, float, int) -> Tuple[List[np.ndarray], np.ndarray]
    """
    packs short partials into longer partials, samples these
    at period `dt` and saved the resulting matrix to a soundfile
    (wav or aif)

    partials: 
        a list of numpy 2D-arrays, each representing a partial
    dt: 
        sampling period to sample the packed partials
    sndfile: 
        path to save the sampled partials. The data is saved
        as an uncompressed soundfile of .wav of .aif format.
    gapfactor: 
        partials are packed with a gap = dt * gapfactor. 
        It should be at least 2
    maxstreams: 
        if > 0, when more streams active than maxstreams, the softest are
        set to zero, which indicates skipping in any subsequent resynthesis
    
    Returns: (packed spectrum, matrix)

    Example
    =======

    partials, labels = read_sdif(sdiffile)
    selected, rest = select(partials, minbps=2, mindur=0.005, minamp=-80)
    partials_save_matrix(selected, 0.002, "packed.wav")
    """
    packed = pack(partials, gap=dt*gapfactor)
    m = partials_sample(packed, dt=dt, maxstreams=maxstreams)
    t0 = min(p[0, 0] for p in partials)
    matrix_save(m, sndfile, dt=dt, t0=t0, bits=32)
    return packed, m


def sndreadmono(path:str, chan:int=0, contiguous=True) -> Tuple[np.ndarray, int]:
    """
    Read a sound file as mono. If the soundfile is multichannel,
    the indicated channel `chan` is returned. 

    path: str
        The path to the soundfile
    chan: int
        The channel to return if the file is multichannel
    contiuous: bool
        If True, it is ensured that the returned array is contiguous
        This should be set to True if the samples are to be
        passed to `analyze`, which expects a continuous array

    Returns: a tuple (samples:np.ndarray, sr:int)
    """
    import pysndfile
    snd  = pysndfile.PySndfile(path)
    data = snd.read_frames(snd.frames())
    sr   = snd.samplerate()
    if len(data.shape) == 0:
        mono = data
    else:
        mono = data[:,chan]
    if contiguous:
        mono = np.ascontiguousarray(mono)
    return (mono, sr)


def plotpartials(partials: List[np.ndarray], downsample:int=1, cmap='inferno', exp=1, 
                 linewidth=2, ax=None):
    """
    Plot the partials in sp using matplotlib

    partials: List
        a list of numpy arrays, each representing a partial
    downsample: int
        If > 1, only one every `downsample` breakpoints will be taken
        into account. 
    cmap:
        a string defining the colormap used, as presented here:
        https://matplotlib.org/users/colormaps.html
    ax:
        A matplotlib axes. If one is passed, plotting will be done to this
        axes. Otherwise a new axes is created

    Returns a matplotlib axes
    """
    try:
        import matplotlib
    except ImportError:
        raise ImportError("matplotlib is not available." 
                          "Install matplotlib to use the plotting routines")
    from . import plot
    return plot.plotpartials(partials, downsample=downsample, cmap=cmap, exp=exp, 
                             linewidth=linewidth, ax=ax)



# -------------------------------------------------------------------

del List, Tuple