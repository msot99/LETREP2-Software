def simple_peak(emg):
    freq = 1925
    wavelength = .005   
    fire = 500
    maximum=[0]
    n=0
    increase=False

    max_samp = 0

    if emg:
        for j in range(fire,int((fire+(.085*1925)))):
            if emg[j]>=maximum[n]:
                if increase:
                    maximum.append(emg[j])
                    increase=False
                    n+=1
                else:
                    maximum[n]=emg[j]
                max_samp=j
            elif j>(max_samp+((wavelength/2)*freq)):
                increase=True

    peak=maximum[-1]

    # Calculate latency of max peak
    max_delay_ms = (max_samp-500)/freq * 1000
    
    return peak, max_delay_ms


