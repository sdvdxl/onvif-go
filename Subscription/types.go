package Subscription

import (
	"encoding/xml"
	"github.com/IOTechSystems/onvif/event"
	"github.com/IOTechSystems/onvif/xsd"
)

// PullMessages Action
type PullMessages struct {
	XMLName string `xml:"tev:PullMessages"`
	// 手动赋值为调用地址
	EndPoint     string       `xml:"-"`
	Timeout      xsd.Duration `xml:"tev:Timeout"`
	MessageLimit xsd.Int      `xml:"tev:MessageLimit"`
}

func (pullMessages PullMessages) GetEndpoint() string {
	return pullMessages.EndPoint
}

// PullMessagesResponse response type
type PullMessagesResponse struct {
	CurrentTime         *xsd.String                 `json:",omitempty" xml:",omitempty"`
	TerminationTime     *xsd.String                 `json:",omitempty" xml:",omitempty"`
	NotificationMessage []event.NotificationMessage `json:",omitempty" xml:",omitempty"`
}

type Unsubscribe struct {
	XMLName  xml.Name `xml:"http://docs.oasis-open.org/wsn/b-2 Unsubscribe"`
	EndPoint string   `xml:"-"`
	Items    []string `xml:",any" json:"items,omitempty"`
}

type UnsubscribeResponse struct {
	XMLName xml.Name `xml:"http://docs.oasis-open.org/wsn/b-2 UnsubscribeResponse"`
	// 手动赋值为调用地址
	EndPoint string   `xml:"-"`
	Items    []string `xml:",any" json:"items,omitempty"`
}

func (unsubscribe Unsubscribe) GetEndpoint() string {
	return unsubscribe.EndPoint
}
