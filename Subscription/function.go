// -*- Mode: Go; indent-tabs-mode: t -*-
//
// Copyright (C) 2022 Intel Corporation
//
// SPDX-License-Identifier: Apache-2.0

// Code generated by gen_commands.py DO NOT EDIT.

package Subscription

type PullMessagesFunction struct{}

func (_ *PullMessagesFunction) Request() interface{} {
	return &PullMessages{}
}
func (_ *PullMessagesFunction) Response() interface{} {
	return &PullMessagesResponse{}
}
