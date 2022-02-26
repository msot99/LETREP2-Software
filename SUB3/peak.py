from scipy import signal
freq=1925

def simple_peak(trialdata):
    freq=1925
    wavelength=.005

    emg=trialdata.emg_data
    acc=trialdata.acc_data

    start_acc=acc[0]

    for i in range(len(acc)):
        if acc[i]!=start_acc:
            fire=i
            break

    maximum=[650]
    maximum[0]=0
    n=0
    increase=False

    for j in range(int((fire+(.04*1925))),int((fire+(.085*1925)))):
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

    return peak


def base_peak(trialdata):

    emg=trialdata.emg_data

    maxes=signal.find_peaks(emg, height=.15)[0]

    peak=maxes[0]

    sum=0
    for i in range((peak-10),(peak+10)):
        sum=sum+emg[i]
    
    avg_peak=sum/20
    peak_ms = (peak-500)/freq * 1000

    return(avg_peak, peak_ms)

def condition_peak(trialdata):
    avg_time=36.36

    M1_avg=(avg_time*freq/1000)+500

    emg=trialdata.emg_data[M1_avg-20:M1_avg+20]

    maxes=signal.find_peaks(emg, height=.1)[0]

    peak=maxes[0]

    sum=0
    for i in range((peak-10),(peak+10)):
        sum=sum+emg[i]

    avg_peak=sum/20
    peak_ms = (peak-500+M1_avg)/freq * 1000

    return(avg_peak, peak_ms)


