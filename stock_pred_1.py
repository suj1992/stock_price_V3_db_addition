import yfinance as yf
import pandas as pd
from flask import Flask, render_template, request, send_from_directory, session

risk = 100
def risk_factor(entry,exit):

    entry = float(request.form.get('fname'))
    exit = float(request.form.get('lname'))

    if entry> exit:
        stop_loss = entry-exit
        quant = risk//stop_loss
        target = stop_loss*2+entry
        total_amount = quant*entry
    else:
        stop_loss = exit-entry
        quant = risk//stop_loss
        target = entry-stop_loss*2
        total_amount = quant*entry



    return entry,exit,quant, target,total_amount, risk