#include <IOKit/pwr_mgt/IOPMLib.h>
#include "sleepless.h"

static IOPMAssertionID gAwakeAssertion = kIOPMNullAssertionID;

/* Keeps OS awake
 */
int sleeplessKeepAwake(CFStringRef cfstr)
{
    if (gAwakeAssertion == kIOPMNullAssertionID) {
        IOPMAssertionCreateWithName(
          kIOPMAssertionTypePreventUserIdleSystemSleep,
          kIOPMAssertionLevelOn,
          cfstr,
          &gAwakeAssertion);
    }
    return(0);
}


/* Let OS sleep
 */
int sleeplessAllowSleep(void)
{
    if (gAwakeAssertion != kIOPMNullAssertionID) {
        IOPMAssertionRelease(gAwakeAssertion);
        gAwakeAssertion = kIOPMNullAssertionID;
    }
    return(0);
}
