#!/usr/bin/env python3
import argparse
import re
import os
import csv
import configparser

class DataStock:
    def __init__(self, price1, price2):
        self.price1 = price1
        self.price2 = price2
        self.amount1 = 0.0
        self.amount2 = 0.0
        self.diffAmount = 0.0
        self.ROI = 0.0;
        self.realProfit = 0.0;

    def getPrice1(self):
        return self.price1

    def setPrice1(self, price):
        self.price1 = price

    def getPrice2(self):
        return self.price2

    def setPrice2(self, price):
        self.price2 = price

    def getAmount1(self):
        return self.amount1

    def setAmount1(self, amount):
        self.amount1 = amount

    def getAmount2(self):
        return self.amount2

    def setAmount2(self, amount):
        self.amount2 = amount

    def getDiffAmount(self):
        return self.diffAmount

    def setDiffAmount(self, diffAmount):
        self.diffAmount = diffAmount

    def getROI(self):
        return self.ROI

    def setROI(self, roi):
        self.ROI = roi

    def getRealProfit(self):
        return self.realProfit

    def setRealProfit(self, realRoi):
        self.realProfit = realRoi
        
#------
class Tools:
    def __init__(self):
        self.original = ","
        self.decimal = "."

    def strToDouble(self,strValue):
        try:
            strNumber = strValue.replace(self.original, self.decimal)
            return float(strNumber)
        except ValueError:
            raise ValueError("Invalid input string. Only numbers and single decimal point are allowed.")

    def getConfig(filename):
        config = configparser.ConfigParser()
        try:
          config.read(filename)
          return config
        except (FileNotFoundError, configparser.Error) as e:
          print(f"Error reading configuration file: {e}")
          return None


#------

if __name__ == '__main__':

    parser = argparse.ArgumentParser(description='Parameters csv file')
    parser.add_argument('-b', '--beg', type=str, required=True, help='csv file with data of begining of the period')
    parser.add_argument('-e', '--end', type=str, required=True, help='csv file with data of end of the period')
    parser.add_argument('-i', '--inflation', type=str, required=True, help='inflation in the period')
    args = parser.parse_args()
    
    try:
        mapStock = dict()
        tool = Tools()

        #Open the begining  CSV file
        with open(args.beg, 'r') as csvfile:
            #Create a reader object
            csv_reader = csv.reader(csvfile)
            header_row = next(csv_reader)
     
            #Iterate through the rows
            for row in csv_reader:
                #Accesss each element in the row
                if row[1] in mapStock:
                    print(f"ERROR: DUPLICATE STOCK:'{row[1]}'")
                else:
                    dataStock = DataStock(row[5].replace(",", "."),"")
                    dataStock.setAmount1(tool.strToDouble(row[3]))
                    mapStock[row[1]] = dataStock


        #Open the ending  CSV file
        with open(args.end, 'r') as csvfile:
            #Create a reader object
            csv_reader = csv.reader(csvfile)
            header_row = next(csv_reader)
     
            #Iterate through the rows
            for row in csv_reader:
                #Accesss each element in the row
                if row[1] in mapStock:

                    mapStock[row[1]].setPrice2(row[5].replace(",", "."))
                    initPrice = tool.strToDouble(mapStock[row[1]].getPrice1())
                    endPrice = tool.strToDouble(mapStock[row[1]].getPrice2())

                    #Calculate  return on Investment(ROI): This is a ratio that expresses the profit(gain)
                    ROI = ((endPrice - initPrice) / initPrice) * 100
                    mapStock[row[1]].setROI(ROI)
                    #Calculate  real profit
                    realProfit = ROI - tool.strToDouble(args.inflation)
                    mapStock[row[1]].setRealProfit(realProfit)

                    mapStock[row[1]].setAmount2(tool.strToDouble(row[3]))
                    diffAmount = mapStock[row[1]].getAmount2() - mapStock[row[1]].getAmount1()
                    mapStock[row[1]].setDiffAmount(diffAmount)
                    

                else:
                    print(f"NEW STOCK:'{row[1]}'")
                    dataStock = DataStock("",row[5].replace(",", "."))
                    dataStock.setAmount2(tool.strToDouble(row[3]))
                    mapStock[row[1]] = dataStock

        # Create a ConfigParser object
        config = configparser.ConfigParser()
        config.read("config.ini") # Read the configuration file
        accionesList = []
        bonosList = []
        letrasList = []
        onsList = []
        fondosciList = []
        cedearsList = []
        etfsList = []

        if config:
          acciones = config['STOCKS']['acciones']
          bonos = config['STOCKS']['bonos']
          letras = config['STOCKS']['letras']
          ons = config['STOCKS']['ons']
          fondosci = config['STOCKS']['fondosci']
          cedears = config['STOCKS']['cedears']
          etfs = config['STOCKS']['etfs']

          accionesList = acciones.split(",")
          bonosList = bonos.split(",")
          letrasList = letras.split(",")
          onsList = ons.split(",")
          fondosciList = fondosci.split(",")
          cedearsList = cedears.split(",")
          etfsList = etfs.split(",")

        else:
          print("Failed to load configuration file.")


        with open("acciones_stocks.csv", 'w') as accionesfile:
            with open("bonos_stocks.csv", 'w') as bonosfile:
                with open("letras_stocks.csv", 'w') as letrasfile:
                    with open("ons_stocks.csv", 'w') as onsfile:
                        with open("cedears_stocks.csv", 'w') as cedearsfile:
                            with open("etfs_stocks.csv", 'w') as etfsfile:
                                with open("fondosci_stocks.csv", 'w') as fondoscifile:
                                    header = f"Stock,Price1,Price2,Amount1,Amount2,DiffAmount,ROI,RealProfit"
                                    accionesfile.write(header + "\n")
                                    bonosfile.write(header + "\n")
                                    letrasfile.write(header + "\n")
                                    onsfile.write(header + "\n")
                                    cedearsfile.write(header + "\n")
                                    etfsfile.write(header + "\n")
                                    fondoscifile.write(header + "\n")

                                    for key, value in mapStock.items():
                                        line = f"{key},{value.getPrice1()},{value.getPrice2()},{value.getAmount1()},{value.getAmount2()},{value.getDiffAmount()},{value.getROI()},{value.getRealProfit()}"

                                        if key in accionesList:
                                            accionesfile.write(line + "\n")
                                        elif key in bonosList:
                                            bonosfile.write(line + "\n")
                                        elif key in letrasList:
                                            letrasfile.write(line + "\n")
                                        elif key in onsList:
                                            onsfile.write(line + "\n")
                                        elif key in cedearsList:
                                            cedearsfile.write(line + "\n")
                                        elif key in etfsList:
                                            etfsfile.write(line + "\n")
                                        elif key in fondosciList:
                                            fondoscifile.write(line + "\n")
                                        else:
                                            print(f"ERROR: the stock:{key}, doesn't exist in ARG stocks or CEDEAR stocks")



    except FileNotFoundError:
        print(f"File '{args.file}' not found.")
    except IOError:
        print(f"Error reading file '{args.file}'.")

