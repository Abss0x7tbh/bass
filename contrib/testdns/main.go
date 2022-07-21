package main

import (
	"bufio"
	"flag"
	"fmt"
	"github.com/sirupsen/logrus"
	"mission/pkg/dns"
	"net"
	"os"
	"sync"
)

func stdinReader() chan string {
	outchan := make(chan string, 1)
	scan := bufio.NewScanner(os.Stdin)
	go func() {
		for scan.Scan() {
			if scan.Err() != nil {
				fmt.Println("Error reading stdin:", scan.Err())
				return
			}
			outchan <- scan.Text()
		}
		close(outchan)
	}()
	return outchan
}

func worker(hostname string, serverChan chan string, resultChan chan *dns.Result) {
	for server := range serverChan {
		r, err := dns.Query(hostname, server)
		if err == nil {
			resultChan <- r
		}else {
			logrus.Debugln(err)
		}
	}
}

var (
	workers  *int
	hostname *string
	verbose  *bool
)

func init() {
	workers = flag.Int("workers", 25, "number of workers")
	hostname = flag.String("hostname", "", "hostname to resolve")
	verbose = flag.Bool("verbose", false, "verbose")
	flag.Parse()
	if *hostname == "" {
		logrus.Errorln("please specify hostname")
		os.Exit(1)
	}
	if *verbose {
		logrus.SetLevel(logrus.DebugLevel)
	}
}

func main() {
	ips, err := net.LookupIP(*hostname)
	if err != nil {
		logrus.Errorf("error resolving %s (%s)", *hostname, err)
		return
	}
	wg := &sync.WaitGroup{}
	serverChan := make(chan string, *workers)
	resultChan := make(chan *dns.Result, *workers)
	for i := 0; i < *workers; i++ {
		go func() {
			wg.Add(1)
			worker(*hostname, serverChan, resultChan)
			wg.Done()
		}()
	}

	go func() {
		oc := stdinReader()
		for line := range oc {
			serverChan <- line
		}
		close(serverChan)
		wg.Wait()
		close(resultChan)
	}()

	for result := range resultChan {
		logrus.Debugln(result)
		out:
		for _, ip := range ips {
			for _, ip2 := range result.Answer {
				if ip.Equal(ip2) {
					fmt.Println(result.Server)
					break out
				}
			}
		}
	}
}
