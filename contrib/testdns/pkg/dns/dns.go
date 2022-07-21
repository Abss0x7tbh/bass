package dns

import (
	"github.com/phuslu/fastdns"
	"net"
	"time"
)

type Result struct {
	Server string
	Question string
	Answer []net.IP
	Time time.Duration
}

func Query(domain, server string) (*Result, error) {
	client := &fastdns.Client{
		ServerAddr:  &net.UDPAddr{IP: net.ParseIP(server), Port: 53},
		ReadTimeout: 2 * time.Second,
		MaxConns:    1000,
	}

	req, resp := fastdns.AcquireMessage(), fastdns.AcquireMessage()
	defer fastdns.ReleaseMessage(req)
	defer fastdns.ReleaseMessage(resp)

	req.SetRequestQustion(domain, fastdns.TypeA, fastdns.ClassINET)

	start := time.Now()
	err := client.Exchange(req, resp)
	if err != nil {
		//fmt.Fprintf(os.Stderr, "client=%+v exchange(\"%s\") error: %+v\n", client, domain, err)
		return nil, err
	}
	end := time.Now()
	result := &Result{
		Server:   server,
		Question: domain,
		Time:     end.Sub(start),
	}
	_ = resp.VisitResourceRecords(func(name []byte, typ fastdns.Type, class fastdns.Class, ttl uint32, data []byte) bool {
		switch typ {
		case fastdns.TypeA, fastdns.TypeAAAA:
			result.Answer = append(result.Answer, net.IP(data))
		}
		return true
	})
	return result, nil
}
