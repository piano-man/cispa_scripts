#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <netinet/in.h>
#include <linux/types.h>
#include <linux/netfilter.h>		
#include <libnetfilter_queue/libnetfilter_queue.h>
#include<limits.h>

struct req_info
{
	int rv;
	u_int32_t id;
	struct nfq_q_handle  *qh;
	char *buf __attribute__ ((aligned)); 
};
struct nfq_q_handle *qh; 
struct req_info packets[1500];
u_int32_t counts[10000];
int count = 0;
int start = 0;
static u_int32_t print_pkt (struct nfq_data *tb)
{
	int id = 0;
	struct nfqnl_msg_packet_hdr *ph;
	struct nfqnl_msg_packet_hw *hwph;
	u_int32_t mark,ifi; 
	int ret;
	unsigned char *data;

	ph = nfq_get_msg_packet_hdr(tb);
	if (ph) {
		id = ntohl(ph->packet_id);
		printf("hw_protocol=0x%04x hook=%u id=%u ",
			ntohs(ph->hw_protocol), ph->hook, id);
	}

	hwph = nfq_get_packet_hw(tb);
	if (hwph) {
		int i, hlen = ntohs(hwph->hw_addrlen);

		printf("hw_src_addr=");
		for (i = 0; i < hlen-1; i++)
			printf("%02x:", hwph->hw_addr[i]);
		printf("%02x ", hwph->hw_addr[hlen-1]);
	}

	mark = nfq_get_nfmark(tb);
	if (mark)
		printf("mark=%u ", mark);

	ifi = nfq_get_indev(tb);
	if (ifi)
		printf("indev=%u ", ifi);

	ifi = nfq_get_outdev(tb);
	if (ifi)
		printf("outdev=%u ", ifi);
	ifi = nfq_get_physindev(tb);
	if (ifi)
		printf("physindev=%u ", ifi);

	ifi = nfq_get_physoutdev(tb);
	if (ifi)
		printf("physoutdev=%u ", ifi);

	ret = nfq_get_payload(tb, &data);
	if (ret >= 0) {
		printf("payload_len=%d ", ret);
		//processPacketData (data, ret);
	}
	fputc('\n', stdout);

	return id;
}
	

static int cb(struct nfq_q_handle *qh, struct nfgenmsg *nfmsg, struct nfq_data *nfa, void *data)
{
	u_int32_t id = print_pkt(nfa);
//	u_int32_t id;

        struct nfqnl_msg_packet_hdr *ph;
	ph = nfq_get_msg_packet_hdr(nfa);	
	id = ntohl(ph->packet_id);
	printf("entering callback\n");
	printf("Printing packet id inside callback : ");
	printf("%d\n",id);
	//struct req_info p;
	//p.id = id;
	//p.qh = qh;
	//packets[count] = p;
	counts[count] = id;
	count++;
	printf("printing count value inside callback : ");
	printf("%d\n",count);
//	return 1;
//	if (count < 4)
//	return nfq_set_verdict(qh, id, NF_ACCEPT, 0, NULL);
//	else 
//	return 1;
	return nfq_set_verdict(qh,id,NF_ACCEPT,0,NULL);
}

	int set_verdict(struct nfq_handle *h)
	{
		printf("Inside set_verdict\n");
		printf("%d\n",count);
		for(int i = count-1 ; i >= 4; i--)
		{
			//struct req_info p = packets[i];
			printf("Printing packet id inside set_verdict : ");
			printf("%d\n",counts[i]);
			//printf("Packet Size inside set_verdict() : ");
			//printf("%d\n",p.rv);
			//nfq_handle_packet(h, p.buf, p.rv); 
			nfq_set_verdict(qh, counts[i], NF_ACCEPT, 0, NULL);
		}
	return 0;

	}

int main(int argc, char **argv)
{
	struct nfq_handle *h;
	//struct nfq_q_handle *qh;
	int fd;
	int rv;
	char buf[4096] __attribute__ ((aligned));

	printf("opening library handle\n");
	h = nfq_open();
	if (!h) {
		fprintf(stderr, "error during nfq_open()\n");
		exit(1);
	}

	printf("unbinding existing nf_queue handler for AF_INET (if any)\n");
	if (nfq_unbind_pf(h, AF_INET) < 0) {
		fprintf(stderr, "error during nfq_unbind_pf()\n");
		exit(1);
	}

	printf("binding nfnetlink_queue as nf_queue handler for AF_INET\n");
	if (nfq_bind_pf(h, AF_INET) < 0) {
		fprintf(stderr, "error during nfq_bind_pf()\n");
		exit(1);
	}

	printf("binding this socket to queue '0'\n");
	qh = nfq_create_queue(h, 1, &cb, NULL);
	nfq_set_queue_maxlen(qh,INT_MAX);
	if (!qh) {
		fprintf(stderr, "error during nfq_create_queue()\n");
		exit(1);
	}

	printf("setting copy_packet mode\n");
	if (nfq_set_mode(qh, NFQNL_COPY_PACKET, 0xffff) < 0) {
		fprintf(stderr, "can't set packet_copy mode\n");
		exit(1);
	}

	fd = nfq_fd(h);

	// para el tema del loss:   while ((rv = recv(fd, buf, sizeof(buf), 0)) && rv >= 0)
	while (count < 9 && (rv = recv(fd, buf, sizeof(buf), 0)))
	{
//		struct req_info p;
//		p.rv = rv;p.buf = buf;
//		packets[count]= p;
		//count++;
		printf("packet received \n");
		printf("packet size in read loop : ");
		printf("%d\n",rv);
		nfq_handle_packet(h, buf, rv);
		//printf("count value inside read loop : ");
		//printf("%d\n",count);
	}
	printf("Outside read loop\n");
	//set_verdict(h);

	printf("unbinding from queue 0\n");
	nfq_destroy_queue(qh);

#ifdef INSANE
	/* normally, applications SHOULD NOT issue this command, since
	 * it detaches other programs/sockets from AF_INET, too ! */
	printf("unbinding from AF_INET\n");
	nfq_unbind_pf(h, AF_INET);
#endif

	printf("closing library handle\n");
	nfq_close(h);

	exit(0);
}
