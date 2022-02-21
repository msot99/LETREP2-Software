from scipy import signal

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

def wave_avg(trialdata):
    emg=trialdata.emg_data

    maxes=signal.find_peaks(emg, height=.06, distance=10)[0]

    print(maxes)

    peak_dis=1000
    for i in range(len(maxes)):
        if(abs(maxes[i]-596)<peak_dis):
            peak_dis=abs(maxes[i]-596)
            peak=maxes[i]

    sum=0
    for i in range((peak-10),(peak+10)):
        sum=sum+emg[i]

    avg_peak=sum/20

    return(avg_peak)


