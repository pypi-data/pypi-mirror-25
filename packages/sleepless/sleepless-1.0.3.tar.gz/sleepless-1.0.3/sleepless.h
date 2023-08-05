#ifndef SLEEPLESS_H_INCLUDED_
#define SLEEPLESS_H_INCLUDED_
#include <CoreFoundation/CoreFoundation.h>
#include <ApplicationServices/ApplicationServices.h>

int sleeplessKeepAwake(CFStringRef cfstr);
int sleeplessAllowSleep(void);

#endif
