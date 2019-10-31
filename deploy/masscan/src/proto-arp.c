#include "proto-arp.h"
#include "proto-preprocess.h"
#include "logger.h"
#include "output.h"
#include "masscan-status.h"
#include "unusedparm.h"



/***************************************************************************
 * Process an ARP packet received in response to an ARP-scan.
 ***************************************************************************/
void
handle_arp(struct Output *out, time_t timestamp, const unsigned char *px,
           unsigned length, struct PreprocessedInfo *parsed)
{
    unsigned ip_them;

    UNUSEDPARM(length);
    UNUSEDPARM(px);

    ip_them = parsed->ip_src[0]<<24 | parsed->ip_src[1]<<16
            | parsed->ip_src[2]<< 8 | parsed->ip_src[3]<<0;

    LOG(3, "ARP %u.%u.%u.%u = [%02X:%02X:%02X:%02X:%02X:%02X]\n",
        parsed->ip_src[0], parsed->ip_src[1],
        parsed->ip_src[2], parsed->ip_src[3],
        parsed->mac_src[0], parsed->mac_src[1], parsed->mac_src[2], 
        parsed->mac_src[3], parsed->mac_src[4], parsed->mac_src[5]);


    output_report_status(
                    out,
                    timestamp,
                    PortStatus_Arp,
                    ip_them,
                    0, /* ip proto */
                    0,
                    0,
                    0,
                    parsed->mac_src);

}
