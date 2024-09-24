package Subscription

import (
	"github.com/IOTechSystems/onvif/event"
	"github.com/IOTechSystems/onvif/xsd"
)

// PullMessages Action
type PullMessages struct {
	XMLName      string       `xml:"tev:PullMessages"`
	EndPoint     string       `xml:"-"`
	Timeout      xsd.Duration `xml:"tev:Timeout"`
	MessageLimit xsd.Int      `xml:"tev:MessageLimit"`
}

// PullMessagesResponse response type
type PullMessagesResponse struct {
	CurrentTime         *xsd.String                 `json:",omitempty" xml:",omitempty"`
	TerminationTime     *xsd.String                 `json:",omitempty" xml:",omitempty"`
	NotificationMessage []event.NotificationMessage `json:",omitempty" xml:",omitempty"`
}
