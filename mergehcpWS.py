import os
import sys
import ROOT
from ROOT import gStyle, TFile, TCanvas, TLegend, TLatex
from argparse import ArgumentParser

from array import array  

ROOT.gROOT.SetBatch(True)
  
from plotting.AtlasStyle import applyAtlasStyle, Style


fileName1 = '/lustre/user/syuen/hadhad/plottingCode_v14/trunk/analysis/hadhad/ws_nOS/1516merged/hhAll_WSinput.root'
fileName2 = '/lustre/user/syuen/hadhad/plottingCode_v14/trunk/analysis/hadhad/ws_nOS/1516merged/hhAll_WSinput.root'

def saveCanvas( canvas ):
	canvas.SaveAs( '%s.png'%canvas.GetName() )

def getInclFake( thisHist, hist_fake_incl, channel ):
  thisIndex = channel.split('_').index('signal')
  decayMode = channel.split('_')[thisIndex+1]
  cbaCat = channel.split('_')[2]
  hcpCat = channel.split('_')[-1]
  #l_cba = ['pres','vbf','boost']

  thisKey = '%s_%s_%s'%(cbaCat,decayMode,hcpCat)

  if 'vbf_ipip' in thisKey: thisKey='vbf_ipip'

  if hist_fake_incl[thisKey] == None:
    hist_fake_incl[thisKey] = thisHist.Clone()
  else:
    hist_fake_incl[thisKey].Add(thisHist,1)

def writeInclFake( dictOfSamplesInChannels_file1, hist_fake_incl ):
  for channel in dictOfSamplesInChannels_file1:
      if 'preselection' in channel: continue
      thisIndex = channel.split('_').index('signal')
      decayMode = channel.split('_')[thisIndex+1]
      cbaCat = channel.split('_')[2]
      hcpCat = channel.split('_')[-1]
      thisKey = '%s_%s_%s'%(cbaCat,decayMode,hcpCat)
      if 'vbf' in thisKey and 'ipip' in thisKey: thisKey='vbf_ipip' 
 
      fileAll.cd(channel+'/Fake')	  
      directoryName = channel+'/Fake'
      hist_name1 = directoryName+"/nominal"
      thisFakeHist = file1.Get(hist_name1).Clone()
      fake_integral = thisFakeHist.Integral(1,thisFakeHist.GetNbinsX()+1)
      thisFakeHistIncl = hist_fake_incl[thisKey].Clone()
      thisFakeHistIncl.Scale(fake_integral/thisFakeHistIncl.Integral(1,thisFakeHistIncl.GetNbinsX()+1))
      #hh_cba_boost_loose_signal_iprho_d0sigy_high
      thisFakeHistIncl.SetTitle('nominal')
      thisFakeHistIncl.SetName('nominal')
      thisFakeHistIncl.Write()

      for key_file1 in range(file1.GetDirectory(directoryName).GetNkeys()):
        #hist_file1 = file1.Get(directoryName+"/"+file1.GetDirectory(directoryName).GetListOfKeys().At(key_file1).GetName())
        #hist_file2 = file2.Get(directoryName+"/"+file1.GetDirectory(directoryName).GetListOfKeys().At(key_file1).GetName())
        hist_name = file1.GetDirectory(directoryName).GetListOfKeys().At(key_file1).GetName()        
        if hist_name.endswith('_high') or 'nominal' in hist_name: continue
        hist_name = hist_name.replace('_low','')
        print channel, '\twrite incl fake hist_name1 ',hist_name

        #2monline
        print 'channel ', channel
        hist_name_sys_low = directoryName+"/%s_low"%hist_name
        print '\t hist_name_sys_low ', hist_name_sys_low
        thisFakeHist_sys_low = file1.Get(hist_name_sys_low).Clone()
        ratio_sys_low = thisFakeHist_sys_low.Clone("%s_sys_%s_low"%(hist_name,channel))
        ratio_sys_low.Divide(thisFakeHist)
        thisFakeHistIncl_sys_low=thisFakeHistIncl.Clone("%s_low"%hist_name)
        thisFakeHistIncl_sys_low.Multiply(ratio_sys_low)

        hist_name_sys_high = directoryName+"/%s_high"%hist_name
        thisFakeHist_sys_high = file1.Get(hist_name_sys_high).Clone()
        ratio_sys_high = thisFakeHist_sys_high.Clone("%s_sys_%s_high"%(hist_name,channel))
        ratio_sys_high.Divide(thisFakeHist)
        thisFakeHistIncl_sys_high=thisFakeHistIncl.Clone("%s_high"%hist_name)
        thisFakeHistIncl_sys_high.Multiply(ratio_sys_high)

        print 'writing sys ', hist_name, ' for channel ', channel
        thisFakeHistIncl_sys_high.Write()
        thisFakeHistIncl_sys_low.Write()

      print ''
      #hh_cba_boost_loose_signal_iprho_d0sigy_high
      #thisFakeHistIncl.Scale(fake_integral/thisFakeHistIncl.Integral(1,thisFakeHistIncl.GetNbinsX()+1))
      #thisFakeHistIncl.Write()
      
#  hist_fake_pres_incl.Print('all')

def drawSigComparePlots( dictOfSamplesInChannels_file1 ):
  print 'drawing sig compare plots'
  for channel in (dictOfSamplesInChannels_file1):
    if 'preselection' in channel: continue
    c1= TCanvas ("c_%s"%channel,"c_%s"%channel,800,650);
    c1.cd()
    directoryName = channel+'/ggH'
    hist_name1 = directoryName+"/nominal"
    sigHist = file1.Get(hist_name1).Clone()
    sigHist.SetDirectory(0)
    sigHist.SetLineColorAlpha(1,.8)
    sigHist.SetMarkerColorAlpha(1,.8)
    sigHist.SetLineWidth(3)
#    sigHist.GetYaxis().SetTitle('Norm to 1')
    sigHist.GetYaxis().SetRangeUser(0,sigHist.GetMaximum()*3)
    sigHist.Draw("E1")
    leg = TLegend(0.50,0.6,0.85,0.9);
    leg.SetNColumns(2);
    thetas = [0,10,20,30,40,50,60,70,80,90,100,110,120,130,140,150,160,170]
    #thetas = [0,20,40,60,80,100,120,140,160]

    thetaHists=[]
    for iTheta, theta in enumerate(thetas):
      #if iTheta%2 !=0: continue
      hist_name_theta = "%s/ggh_unpol_theta_%i/nominal"%(channel,theta)
      thetaHist = file1.Get(hist_name_theta).Clone('%s_%s'%(channel,theta))
      thetaHist.SetTitle('%s_%s'%(channel,theta))
      print '\thist_name_theta ', thetaHist.GetName(), '\t ', thetaHist.GetTitle()
      thetaHist.SetDirectory(0)
      thetaHist.SetLineColorAlpha(31+iTheta*3,.8)
      thetaHist.SetMarkerColorAlpha(31+iTheta*3,.8)
      thetaHists.append(thetaHist.Clone("%s_%i_%i"%(channel,theta,iTheta)))

    c1.cd()
    for iTheta, theta in enumerate(thetaHists):
      theta.Draw('E1 same')
      leg.AddEntry(theta,'ggH %i'%thetas[iTheta],"pel")  
    leg.SetHeader(channel)
    leg.SetBorderSize(0);
    leg.SetFillStyle(0);
    leg.SetTextSize(0.03)
    leg.AddEntry(sigHist,'Nominal',"pel")

    leg.Draw("same")
    c1.SaveAs("%s/plots/SigCompare_%s.pdf"%(result.inputpath,channel))
    #c1.Write("%s/plots/SigCompare_%s.pdf"%(result.inputpath,channel))

def drawFakeComparePlots( dictOfSamplesInChannels_file1 , hist_fake_incl):
  cans = {}
  legs = {}
  hists = {}
  for channel in dictOfSamplesInChannels_file1:
    if 'preselection' in channel: continue
    thisIndex = channel.split('_').index('signal')
    decayMode = channel.split('_')[thisIndex+1]
    cbaCat = channel.split('_')[2]
    hcpCat = channel.split('_')[-1]
    thisKey = '%s_%s_%s'%(cbaCat,decayMode,hcpCat)
    if 'vbf' in thisKey and 'ipip' in thisKey: thisKey='vbf_ipip'
    if thisKey not in cans: 
      hists[thisKey] = []
      c1= TCanvas ("c_%s"%thisKey,"c_%s"%thisKey,800,650);
      c1.cd()
      thisFakeHistIncl = hist_fake_incl[thisKey].Clone(thisKey)
      thisFakeHistIncl.SetDirectory(0)
      thisFakeHistIncl.SetLineColorAlpha(1,1)
      thisFakeHistIncl.SetMarkerColorAlpha(1,1)
      thisFakeHistIncl.GetYaxis().SetTitle('Norm to 1')
      thisFakeHistIncl.GetYaxis().SetRangeUser(0,thisFakeHistIncl.GetMaximum()*1.3)
      thisFakeHistIncl.Scale(1/thisFakeHistIncl.Integral(1,thisFakeHistIncl.GetNbinsX()+1))
      thisFakeHistIncl.Draw()
      cans[thisKey] = c1.Clone(thisKey)
    if thisKey not in legs: 
      leg = TLegend(0.50,0.7,0.85,0.9);
      leg.SetHeader(thisKey)
      leg.SetBorderSize(0);
      leg.SetFillStyle(0);
      leg.SetTextSize(0.03)
      leg.AddEntry(thisFakeHistIncl,'Nominal',"pel")
      legs[thisKey] = leg

  for iColor, channel in enumerate(dictOfSamplesInChannels_file1):
    if 'preselection' in channel: continue
    thisIndex = channel.split('_').index('signal')
    decayMode = channel.split('_')[thisIndex+1]
    cbaCat = channel.split('_')[2]
    hcpCat = channel.split('_')[-1]
    thisKey = '%s_%s_%s'%(cbaCat,decayMode,hcpCat)
    if 'vbf' in thisKey and 'ipip' in thisKey: thisKey='vbf_ipip'

    directoryName = channel+'/Fake'
    hist_name1 = directoryName+"/nominal"
    thisFakeHist = file1.Get(hist_name1).Clone(channel)
    thisFakeHist.SetDirectory(0)
    cans[thisKey].cd()
    thisFakeHist.SetMarkerColorAlpha(iColor,.8)
    thisFakeHist.SetLineColorAlpha(iColor,.8)
    thisFakeHist.Scale(1/thisFakeHist.Integral(1,thisFakeHist.GetNbinsX()+1))
    thisFakeHist.GetYaxis().SetRangeUser(0,thisFakeHist.GetMaximum()*1.3)
    hists[thisKey].append(thisFakeHist.Clone("h_"+channel))
#    thisFakeHist.Draw("same")
#    legs[thisKey].AddEntry(thisFakeHist,channel.replace("hh_cba_",""),"pel")
#    print 'drew ', hist_name1

#  print 'cans ', cans
  for key, value in cans.items():
    print key, '\t ', value
    value.cd()
    theseHists = hists[key]
    print 'theseHists ', theseHists
    for iHist,hist in enumerate(theseHists):
      hist.Clone('%s_%i'%(key,iHist))
      value.cd()
      hist.Draw("E1 same")
      hist.GetYaxis().SetRangeUser(0,1)
      legs[key].AddEntry(hist,hist.GetTitle(),"lep")
    legs[key].Draw("same")
    value.SaveAs("%s/plots/FakeCompare_%s.pdf"%(result.inputpath,key))


def drawZComparePlots( hist_data_Z, hist_mc_Z, channel, hist_data_Z_integral, hist_mc_Z_integral, hist_data_Z_entries, hist_mc_Z_entries):
      c= TCanvas("c_%s"%channel,"c_%s"%channel,800,650);
      c.cd()
      leg = TLegend(0.20,0.8,0.9,0.9);
      leg.SetBorderSize(0);
      leg.SetFillStyle(0);
      leg.SetTextSize(0.03)
#      hist_data_Z.Scale(1/hist_data_Z_integral)
#      hist_mc_Z.Scale(1/hist_mc_Z_integral)
      ymax = max(hist_mc_Z.GetMaximum(),hist_data_Z.GetMaximum())*2
      ymin = min(hist_mc_Z.GetMinimum(),hist_data_Z.GetMinimum())*.05
#      print 'hist_mc_Z.GetMaximum() ', hist_mc_Z.GetMaximum(), '\t hist_data_Z.GetMaximum() ', hist_data_Z.GetMaximum(), '\t ', ymax
      hist_data_Z.SetMaximum(ymax)
      hist_mc_Z.SetMaximum(ymax)
      hist_data_Z.SetMinimum(ymin)
      hist_mc_Z.SetMinimum(ymin)
      hist_data_Z.Draw("LP")
      hist_mc_Z.Draw("LP same")
      hist_mc_Z.SetLineColorAlpha(2,.75)
      hist_mc_Z.SetMarkerColorAlpha(2,.75)
      hist_data_Z.SetLineColor(4)
      hist_data_Z.SetLineWidth(4)
      hist_data_Z.SetMarkerColor(4)
      
#      print 'integralanderror ', hist_data_Z.GetIntegralError(1,hist_data_Z.GetNbinsX()+1)
      leg.SetHeader(channel.replace("hh_cba_",""))
      leg.AddEntry(hist_data_Z,"Z from Data scaled to %.2f (Intgl=%.2f, Entries=%.2f)"%(hist_mc_Z_integral,hist_data_Z_integral, hist_data_Z_entries),"LP")
      leg.AddEntry(hist_mc_Z,"Z from MC (Intgl=%.2f, Entries=%.2f)"%(hist_mc_Z_integral, hist_mc_Z_entries),"LP")
      leg.Draw()
      c.SaveAs("%s/plots/ZttCompare_%s.pdf"%(result.inputpath,channel))
#Data:
#Boost IPIP hi
#Boost IPIP lo
#Boost IPRHO hi
#Boost IPRHO lo
#Boost RHORHO hi
#Boost RHORHO lo
class CatMgr():
    '''
    Merges CBA categories for each background
    '''
    #____________________________________________________________
    def __init__(self):
          self.cba = ['boost', 'vbf']
          self.cats = [
              'ipip_d0sig_high',
              'ipip_d0sig_low',
              'iprho_d0sigy_high',
              'iprho_d0sigy_low',
              'rhorho_y0y1_high',
              'rhorho_y0y1_low',
            ]

    def sortSample(self, channel, sample):
           print 'sorting sample'

############# Make Plots ##############
# Apply ATLAS Style
ROOT.gROOT.ProcessLine( 'SetAtlasStyle()' )

setPalette()


if __name__ == '__main__':
  parser = ArgumentParser()
  parser.add_argument('-in', '--inputpath',     type=str)
  parser.add_argument('-ex', '--exclusiveCat',     action='store_true')
  parser.add_argument('-z', '--dataDrivenZregion',     action='store_true')
  parser.add_argument('-mcba', '--mergeCBA',     action='store_true')
  parser.add_argument('-test', '--test',     action='store_true')
  parser.add_argument('-sig', '--sig',     action='store_true')

  result = parser.parse_args()

  if result.inputpath: 
    fileName1='%s/hsr/hhAll_merged_WSinput.root'%result.inputpath
    fileName2='%s/zr/hhAll_merged_WSinput.root'%result.inputpath

  print 'hsr ', fileName1
  print 'zr ', fileName2
  # Load file
  file1 = ROOT.TFile.Open( fileName1 )
  if result.dataDrivenZregion: file2 = ROOT.TFile.Open( fileName2 )
  assert( file1 )
  if result.dataDrivenZregion: assert( file2 )

  #outputHistFile = ROOT.TFile.Open("files/compareInput_output.root", "RECREATE")

  # Collect channels in file1 samples in each channel
  dictOfSamplesInChannels_file1 = {}
  channelKeyList = file1.GetListOfKeys()
  iter = channelKeyList.MakeIterator()
  for channel in range(channelKeyList.GetEntries()):
  #  if not channelKeyList.At(channel).GetName().__contains__("hists"):
  #    continue
    listOfSamplesInChannel = []
    directory = file1.GetDirectory(channelKeyList.At(channel).GetName())
    sampleKeyList = directory.GetListOfKeys()
    for sampleKey in range(sampleKeyList.GetEntries()):
      listOfSamplesInChannel.append(sampleKeyList.At(sampleKey).GetName())
    dictOfSamplesInChannels_file1[channelKeyList.At(channel).GetName()] = listOfSamplesInChannel

#  print "\ndictOfSamplesInChannels_file1 = ", dictOfSamplesInChannels_file1


  # Both dictionories now contain the same channels and samples. Now compare the histograms 
  print "\nStart combining Z and Higgs SR\n"
  errordict  = dict()
  missing = []
  unequalbins = []
  normerr = []
  kserr = []
  errordict["missing"] = missing
  errordict["unequalbins"] = unequalbins
  errordict["normerr"] = normerr
  errordict["kserr"] = kserr

#  os.system('mkdir -p '+wsinAll)
  if result.exclusiveCat: wsOutName = 'hhAll_merged_WSinput.root'
  else: 
    if result.dataDrivenZregion:
      wsOutName = 'hhAll_merged_WSinput_inclfakes.root'
    else:
      wsOutName = 'hsr/hhAll_merged_WSinput_inclfakes.root'
  if result.sig: wsOutName+='sig'
  mergedname=result.inputpath+'/'+wsOutName
  fileAll=TFile(mergedname, 'RECREATE')

  hist_fake_incl = {}
  l_cats = ['low','high']
  l_cba = ['vbf','boost']
  decayModes = ['ipip','iprho','rhorho']
  for cba in l_cba:
    for decayMode in decayModes:
      if cba == 'vbf' and decayMode == 'ipip': 
        hist_fake_incl['vbf_ipip'] = None
        continue
      for l_cat in l_cats:
        hist_fake_incl['%s_%s_%s'%(cba,decayMode,l_cat)] = None  


  if result.sig: 
    drawSigComparePlots( dictOfSamplesInChannels_file1 )
    sys.exit()

  for channel in dictOfSamplesInChannels_file1:
    samples_file1 = dictOfSamplesInChannels_file1[channel]
    hist_data_Fake = None
    hist_data_Z = None
    hist_mc_Z = None
    hist_data_Other = None
    fileAll.mkdir(channel)
    for sample in samples_file1:

      #catmgr = CatMgr()
      #catmgr.sortSample(channel,sample)

      directoryName = channel+'/'+sample
#      print "\nDirectory = ",directoryName

      hists_file1 = []
      if directoryName.__contains__('lumiininvpb'): 
        hists_file1.append( file1.Get( directoryName ) )
        fileAll.cd(channel)
        file1.Get(directoryName).Write()
      else:
        fileAll.mkdir(directoryName)
        fileAll.cd(directoryName)

        for key_file1 in range(file1.GetDirectory(directoryName).GetNkeys()):
          #hist_file1 = file1.Get(directoryName+"/"+file1.GetDirectory(directoryName).GetListOfKeys().At(key_file1).GetName())
          #hist_file2 = file2.Get(directoryName+"/"+file1.GetDirectory(directoryName).GetListOfKeys().At(key_file1).GetName())
          hist_name1 = directoryName+"/"+file1.GetDirectory(directoryName).GetListOfKeys().At(key_file1).GetName()
          thisHist = file1.Get(hist_name1).Clone()
          thisHist.SetDirectory(0)
          if sample == "Fake" and 'nominal' in hist_name1 and not result.exclusiveCat:
            if not 'preselection' in channel:
              getInclFake( thisHist, hist_fake_incl, channel )
	
          #print 'sample ', sample, '\thistname1 ', hist_name1
          if not 'nominal' == hist_name1.split('/')[-1]: 
            if result.exclusiveCat:
              thisHist.Write()
              continue
            else:
              if (not 'extrap' in hist_name1) and (result.dataDrivenZregion and sample=='Ztt' and 'nominal' in hist_name1):
                thisHist.Write()
                continue

          if sample == 'Ztt':
            if result.dataDrivenZregion:
              if 'preselection' in channel:
                print 'not using data driven Z for ', channel
                thisHist.Write()
              else:
                hist_mc_Z = thisHist.Clone()
            else:
              thisHist.Write()
          elif sample == 'Fake':
            if not result.exclusiveCat and 'preselection' in channel: thisHist.Write()
            if result.exclusiveCat: thisHist.Write()
          else:
            thisHist.Write()

    if result.dataDrivenZregion:
      if file2.Get(channel+"/Data/nominal"):
        hist_data_Z = file2.Get(channel+"/Data/nominal").Clone()
        hist_data_Z.SetDirectory(0)
      if file2.Get(channel+"/Fake/nominal"):
        hist_data_Fake = file2.Get(channel+"/Fake/nominal").Clone()
        hist_data_Fake.SetDirectory(0)
      if file2.Get(channel+"/Other/nominal"):
        hist_data_Other = file2.Get(channel+"/Other/nominal").Clone()
        hist_data_Other.SetDirectory(0)

    #print directoryName 
    if result.dataDrivenZregion:
      if 'preselection' in channel: continue
      if not hist_data_Z: print 'missing Z'
      if not hist_data_Fake: print 'missing Fake'
      if not hist_data_Other: print 'missing Other'
      hist_data_Z_integral = hist_data_Z.Integral(1,hist_data_Z.GetNbinsX()+1)
      hist_data_Z_entries = hist_data_Z.GetEntries()
#      print 'before sub hist_data_Z_integral ', hist_data_Z_integral, '\t hist_data_Z_entries ', hist_data_Z_entries
#      print '\t hist_data_Fake integral ', hist_data_Fake.Integral(1,hist_data_Fake.GetNbinsX()+1), ' entires ', hist_data_Fake.GetEntries()
#      print '\t hist_data_Other integral ', hist_data_Other.Integral(1,hist_data_Other.GetNbinsX()+1), ' entires ', hist_data_Other.GetEntries()
      hist_data_Z.Add(hist_data_Fake,-1)
      hist_data_Z.Add(hist_data_Other,-1)
      hist_mc_Z_integral = hist_mc_Z.Integral(1,hist_mc_Z.GetNbinsX()+1)
      hist_mc_Z_entries = hist_mc_Z.GetEntries()
      hist_data_Z_integral = hist_data_Z.Integral(1,hist_data_Z.GetNbinsX()+1)
      hist_data_Z_entries = hist_data_Z.GetEntries()
#      print 'hist_mc_Z_integral ', hist_mc_Z_integral, '\t hist_data_Z_integral ', hist_data_Z_integral
#      print 'hist_mc_Z_entries ', hist_mc_Z_entries, '\t hist_data_Z_entries ', hist_data_Z_entries
      hist_data_Z.Scale(hist_mc_Z_integral/hist_data_Z_integral)
      if hist_data_Z.GetEntries()<.01: 
        print 'hist_data_Z.GetEntries()=',hist_data_Z.GetEntries(), "\t write MC instead"
        hist_data_Z=hist_mc_Z.Clone()
      fileAll.cd(channel+'/Ztt')
      hist_data_Z.Write()    

      drawZComparePlots( hist_data_Z, hist_mc_Z, channel, hist_data_Z_integral, hist_mc_Z_integral, hist_data_Z_entries, hist_mc_Z_entries)
#      print 'hist_mc_Z_integral ', hist_mc_Z_integral, '\t hist_data_Z_integral ', hist_data_Z.Integral(1,hist_data_Z.GetNbinsX()+1)

 
  if not result.exclusiveCat:
    writeInclFake( dictOfSamplesInChannels_file1, hist_fake_incl )

  if result.test:
    drawFakeComparePlots( dictOfSamplesInChannels_file1 , hist_fake_incl)
    print 'done with drawFakeComparePlots'
 
