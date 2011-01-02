#!/bin/bash
fab $@ | tee -a run.log
