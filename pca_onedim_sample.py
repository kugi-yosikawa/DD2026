import numpy as np
import matplotlib.pyplot as plt

im=2                  # Number of Observation Points
nm=64                 # Number of Observation Time
mm=im                 # Number of Mode


#
# Allocate Arrays
#

obsdat=np.zeros([im,nm])   # Observed Data
scores=np.zeros([mm,nm])   # Score

#
# Define Observed Value
#

## Systematic Purtrubation
for i in range(im) :
    obsdat[i,:]=2-i
for n in range(nm) :
    obsdat[:,n]=obsdat[:,n] \
        *(np.sin(2.0*np.pi/nm*n) \
          +np.sin(4.0*np.pi/nm*n) \
          +np.sin(8.0*np.pi/nm*n) \
          )

## Isolated Purtrubation
#for n in range(nm) :
#    obsdat[0,n]=np.sin(2.0*np.pi/nm*n)
#    obsdat[1,n]=np.cos(8.0*np.pi/nm*n)
#    obsdat[1,n]=obsdat[1,n]+obsdat[0,n]
#    obsdat[0,n]=np.max(np.sin(2.0*np.pi/nm*n),0.)
#    obsdat[1,n]=np.abs(np.sin(2.0*np.pi/nm*n))

#
#
# Add Random Perturbation
#
rng=np.random.default_rng()
for i in range(im):
    obsdat[i,:]=obsdat[i,:]+0.5*rng.random(nm)


#
# Extract Mean
#
obsdat[0,:]=obsdat[0,:]-np.mean(obsdat[0,:])
obsdat[1,:]=obsdat[1,:]-np.mean(obsdat[1,:])


#
# Calculate Covariance Matrix
#
covari=np.cov(obsdat[0,:],obsdat[1,:])

#
# Calculate Eigen value and Vector of Covariance Matrix
#
eigval, eigvec = np.linalg.eigh(covari)

#
# Sort Eigen values and vectors according to Eigen values
#
i=np.argsort(eigval)
i=i[::-1] # Reverse order
eigval=eigval[i]
eigvec=eigvec[:,i]

#
# Calculate Score Vector
# (Score = Product between Structure Vector and Observed Data at time
#  step n)
#
for m in range(mm) :
    for n in range(nm) :
        scores[m,n]=np.sum(eigvec[:,m]*obsdat[:,n])



#
# Draw Observed Variables
#

#
# Plot Observed Values (animation)
#
for n in range(nm) :
    fig, figa = plt.subplots(figsize=(8,6),ncols=1,nrows=1)

    figa.plot(obsdat[:,n],marker='o')
    figa.set_xlim(-1,2)
    figa.set_ylim(np.min(obsdat),np.max(obsdat))
    figa.set_xlabel('Observed Location')
    figa.set_ylabel('Observed Values')
    fig.tight_layout()
    fig.savefig('obsdat{:02}'.format(n)+'.jpg')


#
# Plot Observed Values (time series)
#
fig, figa = plt.subplots(figsize=(8,6),ncols=1,nrows=1)
figa.plot(obsdat[0,:],color='red')
figa.plot(obsdat[1,:],color='blue')
figa.set_xlabel('time')
figa.set_ylabel('observed values')

fig.show()
fig.savefig('obsdat_timser.jpg')

#
# Plot Observed Values (scatter) + Eigen Vectors
#
fig, figa = plt.subplots(figsize=(8,6),ncols=1,nrows=1)
figa.scatter(obsdat[0,:],obsdat[1,:],marker='o')
figa.plot([0.,eigvec[0,0]],[0,eigvec[1,0]],color='red')
figa.plot([0.,eigvec[0,1]],[0,eigvec[1,1]],color='blue')
figa.set_xlim(1.1*np.min(obsdat),1.1*np.max(obsdat))
figa.set_ylim(1.1*np.min(obsdat),1.1*np.max(obsdat))
figa.set_xlabel('data @ l=1')
figa.set_ylabel('data @ l=2')
figa.set_aspect('equal', adjustable='box')

fig.show()
fig.savefig('obsdat_scattr.jpg')


#
# Plot First and Second Mode Score
#
#
fig, figa = plt.subplots(figsize=(8,6),ncols=1,nrows=1)
figa.plot(scores[0,:],color='red')
figa.plot(scores[1,:],color='blue')
figa.set_xlabel('time')
figa.set_ylabel('score')

fig.show()
fig.savefig('scores_timser.jpg')


#
# Print Factor Loading
#
print(eigval/np.sum(eigval))
