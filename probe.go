package main
import (
	"fmt"
	"ntp"
	//"strconv"
	"bufio"
	"log"
	"os"
	p "path"
	"runtime"
)

func main(){
	_, filename, _, ok := runtime.Caller(0)
	if !ok {
		println("No caller information")
		os.Exit(-1)
	}
	outputFileName := p.Join(p.Dir(filename), "non_responsive_4.txt")
	file, err := os.Create(outputFileName)
	if err!= nil {
		fmt.Println(err.Error())
	}
	defer file.Close()
	var c int = 1000
	//list := [6]string{"addr_eu.txt","addr_na.txt","addr_asia.txt","addr_oceania.txt","addr_africa.txt","addr_sa.txt"}
	list := [1]string{"addr_global.txt"}
	for _,i := range list {

		f, err := os.Open(i)
		if err != nil {
			log.Fatal(err)
		}
		defer func() {
			if err = f.Close(); err != nil {
				log.Fatal(err)
			}
		}()
		s := bufio.NewScanner(f)
		for s.Scan() {
			fmt.Println(s.Text())
			h := fmt.Sprintf("%x",c)
		//	fmt.Println(h)
			options := ntp.QueryOptions{LocalAddress: "2a01:4f8:c0c:86eb::"+h}
			response, err := ntp.QueryWithOptions(s.Text(), options)
			c += 1
			if err != nil {
				fmt.Println("error")
				file.WriteString("Server: "+s.Text()+"\t"+"Client: "+"2a01:4f8:c0c:86eb::"+h+"\n")
			}
			fmt.Println(response)
		}
		err = s.Err()
		if err != nil {
			log.Fatal(err)
		}
	}
	fmt.Println(c)
}


