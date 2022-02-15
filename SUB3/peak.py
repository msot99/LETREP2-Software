from trial import trial

freq=1925
wavelength=.005

emg=trial.emg_data
acc=trial.acc_data

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

# if peak>=1:
#     print("Noise")
# elif peak<=.1:
#     print("Unsecure")
# else:
#     print(peak)


