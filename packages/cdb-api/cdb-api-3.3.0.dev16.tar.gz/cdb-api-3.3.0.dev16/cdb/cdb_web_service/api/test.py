from cdb.cdb_web_service.api.itemRestApi import ItemRestApi
from cdb.cdb_web_service.api.propertyRestApi import PropertyRestApi

cdbUser = 'cdb'
cdbPass = 'cdb'
cdbHost = '127.0.0.1'
cdbPort = 10232
cdbProtocol = 'http'

itemRestApi = ItemRestApi(cdbUser, cdbPass, cdbHost, cdbPort, cdbProtocol)
propertyRestApi = PropertyRestApi(cdbUser, cdbPass, cdbHost, cdbPort, cdbProtocol)

var = {'S37FB:bpm3:y:Selected': 'S37B:P3', 'S15FB:bpm3:y:Selected': 'S15B:P4',
'S18FB:bpm1:y:Selected': 'S18A:P4', 'S30FB:bpm2:y:Selected': 'S30B:P5',
'S7FB:bpm2:x:Selected': 'S7B:P5', 'S29FB:bpm1:x:Selected': 'S29A:P2',
'S7FB:bpm1:y:Selected': 'S7A:P2', 'S34FB:bpm4:x:Selected': 'S34B:P0',
'S4FB:bpm1:y:Selected': 'S4A:P2', 'DP:EnableWriteXbpmSetPt2RMC': 0L,
'DaqReferenceUnixTime': 1505854568.735395, 'DP:RC:x': 0L, 'DP:RC:y': 0L,
'S9FB:bpm3:y:Selected': 'S9B:P3', 'S5FB:bpm3:x:Selected': 'S5A:P0',
'FileTimeStamp': 'Wed Sep 20 10:46:07 2017 ',
'DP:S:OrbitControlLawYSDDS_CMND': 0L, 'S35FB:bpm4:x:Selected': '16',
'S16FB:bpm4:x:Selected': 'S16B:P0', 'S31FB:bpm4:y:Selected': 'S31B:P3',
'S37FB:bpm1:x:Selected': 'S37A:P2', 'S12FB:bpm1:x:Selected': 'S12A:P2',
'S14FB:bpm1:x:Selected': 'S14B:P5', 'S17FB:bpm2:y:Selected': 'S17B:P3',
'S30FB:bpm4:y:Selected': '16', 'S30FB:bpm3:y:Selected': 'S30B:P2',
'S17FB:bpm4:x:Selected': 'S17B:P0', 'fileModificationTime': 1505922369,
'SRFB:SamplingFreq': 1534.1759956755, 'S23FB:bpm2:y:Selected':
'S23B:P4', 'S8FB:bpm1:x:Selected': 'S8B:P5', 'DaqId': 'DAQ:RTFB',
'S3FB:bpm2:x:Selected': 'S3B:P2', 'DP:S:OrbitControlLawXSDDS_CMND': 0L,
'S18FB:bpm2:y:Selected': 'S18B:P3', 'S20FB:bpm1:x:Selected': 'S20B:P5',
'S30FB:bpm2:x:Selected': 'S30B:P5', 'S6FB:bpm4:x:Selected': 'S6B:P0',
'S36FB:bpm2:y:Selected': 'S36B:P5', 'S30FB:bpm1:y:Selected': 'S30A:P2',
'S2FB:bpm1:x:Selected': 'S2A:P2', 'S10FB:bpm4:x:Selected': 'S10B:P0',
'S14FB:bpm4:y:Selected': 'S14B:P0', 'DP:EnableWriteYbpmSetPt2RMC': 0L,
'S19FB:bpm1:y:Selected': 'S19A:P2', 'S28FB:bpm3:x:Selected': 'S28B:P3',
'dataDirectory': '/net/helios/ctlsdaq1/data', 'S26FB:bpm2:y:Selected':
'S26B:P4', 'S34FB:bpm3:y:Selected': 'S34B:P3', 'S38FB:bpm3:x:Selected':
'S38B:P2', 'S18FB:bpm3:y:Selected': 'S18A:P0', 'S8FB:bpm4:x:Selected':
'16', 'S19FB:bpm4:y:Selected': 'S19B:P0', 'S3FB:bpm4:y:Selected': '16',
'S24FB:bpm2:x:Selected': 'S24B:P3', 'S17FB:bpm1:y:Selected': 'S17B:P4',
'fileCreationTimestamp': '2017/09/20 10:46:09 CDT', 'DaqBurstProtocol':
'TCP', 'S10FB:bpm2:x:Selected': 'S10B:P3', 'S35DCCT:currentCC':
-0.0058722844414, 'S12FB:bpm1:y:Selected': 'S12A:P2',
'S22FB:bpm2:y:Selected': 'S22B:P3', 'S33FB:bpm3:y:Selected': 'S33A:P0',
'DaqFirstArrayId': 7733769L, 'S26FB:bpm1:y:Selected': 'S26A:P2',
'S30FB:bpm4:x:Selected': 'S30B:P2', 'S12FB:bpm2:x:Selected': 'S12A:P4',
'S21FB:bpm1:x:Selected': 'S21A:P4', 'S34FB:bpm1:x:Selected': 'S34B:P5',
'S32FB:bpm1:x:Selected': 'S32B:P5', 'S31FB:bpm2:y:Selected': 'S31B:P5',
'S25FB:bpm3:y:Selected': 'S25A:P0', 'S3FB:bpm3:y:Selected': 'S3B:P2',
'S31FB:bpm4:x:Selected': '16', 'S40FB:bpm2:y:Selected': 'S40B:P3',
'S24FB:bpm2:y:Selected': 'S24B:P3', 'fileSize': 6310021,
'S13FB:bpm1:x:Selected': 'S13A:P2', 'S24FB:bpm4:y:Selected': 'S24B:P0',
'S23FB:bpm4:y:Selected': 'S23B:P0', 'S6FB:bpm4:y:Selected': '16',
'S5FB:bpm3:y:Selected': 'S5B:P2', 'DaqBurstName': '20170920104607001',
'S40FB:bpm1:x:Selected': 'S40A:P2', 'DaqBurstProducerName':
'DAQ:RTFB:STREAM:TCP', 'S7FB:bpm4:y:Selected': '16',
'S9FB:bpm3:x:Selected': 'S9A:P0', 'S27FB:bpm1:y:Selected': 'S27A:P2',
'S29FB:bpm2:x:Selected': 'S29A:P4', 'S8FB:bpm2:y:Selected': 'S8B:P3',
'S36FB:bpm4:x:Selected': 'S36B:P2', 'S21FB:bpm2:y:Selected': 'S21B:P2',
'DaqFirstRowUnixTime': 1505854568.735395, 'S6FB:bpm1:x:Selected':
'S6B:P5', 'S29FB:bpm4:x:Selected': 'S29B:P3', 'SRFB:Kd:y': 0.0,
'SRFB:Kd:x': 0.0, 'S4FB:bpm2:y:Selected': 'S4A:P4',
'S27FB:bpm2:x:Selected': 'S27A:P4', 'S9FB:bpm2:y:Selected': 'S9B:P4',
'S28FB:bpm4:y:Selected': 'S28B:P2', 'S15FB:bpm3:x:Selected': 'S15A:P0',
'S22FB:bpm2:x:Selected': 'S22B:P3', 'S22FB:bpm3:y:Selected': 'S22B:P2',
'S26FB:bpm4:x:Selected': 'S26B:P0', 'DP:DesThres:y': 0.0,
'DP:DesThres:x': 1.0, 'S36FB:bpm2:x:Selected': 'S36B:P5',
'NumberOfBurstsInStream': 1L, 'S34FB:bpm1:y:Selected': 'S34A:P2',
'S38FB:bpm2:x:Selected': 'S38B:P3', 'FileFormatVersion': 'RTFB_DATA_V1',
'S4FB:bpm3:x:Selected': 'S4A:P0', 'S12FB:bpm3:y:Selected': '16',
'S8FB:bpm3:y:Selected': '16', 'DaqBurstDescription': '< user comment >',
'DaqBurstSequenceNumber': 1L, 'S5FB:bpm4:y:Selected': 'S5B:P0',
'S40FB:bpm1:y:Selected': 'S40A:P2', 'S39FB:bpm1:x:Selected': 'S39A:P2',
'experimentName': u'Demo-20170919-10', 'S26FB:bpm1:x:Selected':
'S26A:P2', 'S17FB:bpm3:y:Selected': 'S17A:P0', 'S34FB:bpm2:x:Selected':
'S34B:P2', 'S15FB:bpm4:x:Selected': 'S15B:P0', 'S12FB:bpm2:y:Selected':
'S12B:P3', 'S6FB:bpm3:y:Selected': 'S6A:P0', 'S28FB:bpm1:x:Selected':
'S28A:P2', 'S10FB:bpm3:x:Selected': 'S10A:P0', 'S35FB:bpm1:x:Selected':
'S35B:P5', 'S29FB:bpm4:y:Selected': 'S29B:P2', 'S5FB:bpm4:x:Selected':
'S5B:P0', 'S1FB:bpm1:y:Selected': 'S1A:P3', 'S13FB:bpm3:y:Selected':
'S13B:P3', 'S35FB:bpm3:y:Selected': 'S35B:P2', 'S7FB:bpm3:y:Selected':
'S7B:P2', 'experimentFilePath':
'2017/09/20/rtfbStream.20170920104607001.sdds', 'S2FB:bpm4:y:Selected':
'S2B:P0', 'S4FB:bpm2:x:Selected': 'S4B:P2', 'S1FB:bpm1:x:Selected':
'S1A:P3', 'DP:EnableWriteHCor2RMC': 0L, 'S8FB:bpm2:x:Selected':
'S8B:P3', 'DaqBurstStartUnixTime': '20170920104607.893417513',
'S38FB:bpm4:y:Selected': '16', 'S27FB:bpm4:x:Selected': '16', u'demo':
u'true', 'S19FB:bpm3:x:Selected': 'S19A:P0', 'S28FB:bpm2:x:Selected':
'S28A:P4', 'S33FB:bpm3:x:Selected': 'S33A:P0',
'DP:VCorrVectorModeC_VAL': 0L, 'S40FB:bpm4:x:Selected': 'S40B:P2',
'S39FB:bpm4:y:Selected': 'S39B:P2', 'S4FB:bpm1:x:Selected': 'S4B:P5',
'SRFB:Ki:y': 0.0, 'S19FB:bpm4:x:Selected': 'S19B:P0',
'S8FB:bpm3:x:Selected': '16', 'DP:Average:y': 1.0, 'DP:Average:x': 1.0,
'S32FB:bpm2:y:Selected': 'S32B:P5', 'S40FB:bpm3:x:Selected': 'S40B:P3',
'S20FB:bpm4:x:Selected': 'S20B:P0', 'S11FB:bpm3:x:Selected': 'S11A:P0',
'S35FB:bpm1:y:Selected': 'S35A:P2', 'S5FB:bpm1:y:Selected': 'S5A:P2',
'S14FB:bpm4:x:Selected': 'S14B:P0', 'S11FB:bpm4:x:Selected': 'S11B:P0',
'SRFB:LowPassFreq:x': 2.6, 'SRFB:LowPassFreq:y': 25.0, 'SRFB:Ki:x': 0.0,
'S31FB:bpm3:y:Selected': 'S31B:P4', 'DP:Interval:y': 0.1,
'S9FB:bpm1:y:Selected': 'S9A:P2', 'S13FB:bpm3:x:Selected': 'S13B:P3',
'S12FB:bpm3:x:Selected': 'S12B:P4', 'S4FB:bpm3:y:Selected': 'S4B:P4',
'S33FB:bpm4:x:Selected': 'S33B:P0', 'NumberOfRows': 3213L,
'S34FB:bpm2:y:Selected': 'S34B:P4', 'S27FB:bpm4:y:Selected': 'S27B:P2',
'S6FB:bpm3:x:Selected': 'S6A:P0', 'S36FB:bpm3:x:Selected': 'S36B:P3',
'S24FB:bpm3:x:Selected': 'S24A:P0', 'S7FB:bpm3:x:Selected': 'S7B:P2',
'S11FB:bpm2:y:Selected': 'S11B:P3', 'S17FB:bpm1:x:Selected': 'S17B:P4',
'S24FB:bpm1:y:Selected': 'S24B:P4', 'S3FB:bpm1:x:Selected': 'S3A:P3',
'S28FB:bpm2:y:Selected': 'S28B:P4', 'S31FB:bpm1:y:Selected': 'S31A:P2',
'DaqSddsColumnIds': 'TimeSinceLastSample,MpsTrip,PosX,P0X,Cp0X',
'S25FB:bpm2:y:Selected': 'S25B:P3', 'S19FB:bpm3:y:Selected': 'S19A:P0',
'S36FB:bpm3:y:Selected': 'S36B:P3', 'S11FB:bpm2:x:Selected': 'S11B:P3',
'S35FB:bpm2:y:Selected': 'S35B:P5', 'DaqAverageRowTimeInterval': 0.0,
'S16FB:bpm1:x:Selected': 'S16B:P5', 'S39FB:bpm2:y:Selected': 'S39A:P4',
'DaqLastRowUnixTime': 1505854568.735395, 'fileProcessingTimestamp':
'2017/09/20 10:46:30 CDT', 'S28FB:bpm3:y:Selected': 'S28B:P3',
'S15FB:bpm4:y:Selected': '16', 'S14FB:bpm3:x:Selected': 'S14A:P0',
'DP:XbpmSetPtVectorModeC_VAL': 0L, 'S25FB:bpm2:x:Selected': 'S25B:P4',
'S14FB:bpm1:y:Selected': 'S14A:P2', 'S21FB:bpm3:x:Selected': 'S21A:P0',
'SRFB:LPFilterEnable': 1L, 'S37FB:bpm3:x:Selected': 'S37B:P3',
'S29FB:bpm3:y:Selected': 'S29B:P3', 'S16FB:bpm3:x:Selected': 'S16A:P0',
'S32FB:bpm4:x:Selected': '16', 'S27FB:bpm1:x:Selected': 'S27A:P2',
'DaqDataDescription': '', 'S10FB:bpm1:y:Selected': 'S10B:P4',
'SRFB:HighPassFreq:y': 10.0, 'SRFB:HighPassFreq:x': 10.0,
'DP:S:OrbitControlLawXSDDS_SUSP': 0L, 'DP:LowPassFreq': 10.0,
'S35FB:bpm3:x:Selected': 'S35A:P0', 'DP:Interval:x': 0.1, 'md5Sum':
'80a25cc4b8849425ad32930a0b8a1458', 'S34FB:bpm3:x:Selected': 'S34A:P0',
'S28FB:bpm1:y:Selected': 'S28A:P2', 'fileName':
'rtfbStream.20170920104607001.sdds', 'DaqDriverName': 'DAQ:RTFB:DRV',
'S31FB:bpm1:x:Selected': 'S31B:P5', 'S19FB:bpm2:y:Selected': 'S19B:P3',
'S29FB:bpm1:y:Selected': 'S29A:P2', 'S18FB:bpm2:x:Selected': 'S18B:P3',
'S37FB:bpm2:y:Selected': 'S37B:P5', 'S23FB:bpm4:x:Selected': 'S23B:P0',
'DaqEstimatedRowTimeInterval': 0.00065189, 'S20FB:bpm4:y:Selected':
'16', 'FloatFormat': 'IEEE', 'S30FB:bpm3:x:Selected': 'S30B:P3',
'S21FB:bpm2:x:Selected': 'S21B:P3', 'S22FB:bpm3:x:Selected': 'S22A:P0',
'DP:YbpmSetPtVectorModeC_VAL': 0L, 'S13FB:bpm1:y:Selected': 'S13A:P2',
'fileProcessingTime': 1505922390.344579, 'S32FB:bpm4:y:Selected':
'S32B:P0', 'S37FB:bpm2:x:Selected': 'S37B:P5', 'S2FB:bpm1:y:Selected':
'S2A:P3', 'S15FB:bpm1:x:Selected': 'S15A:P4', 'S30FB:bpm1:x:Selected':
'S30A:P2', 'S15FB:bpm2:y:Selected': 'S15A:P4', 'DP:Gain:x': 0.4,
'DP:Gain:y': 0.4, 'S26FB:bpm2:x:Selected': 'S26B:P5', 'DP:SamplingFreq':
1534.2, 'S6FB:bpm1:y:Selected': 'S6B:P5', 'S32FB:bpm3:x:Selected':
'S32B:P0', 'S1FB:bpm2:y:Selected': 'S1B:P5', 'S32FB:bpm1:y:Selected':
'S32A:P4', 'S10FB:bpm3:y:Selected': 'S10A:P0',
'DP:HCorrVectorModeC_VAL': 0L, 'S23FB:bpm1:y:Selected': 'S23A:P2',
'S39FB:bpm2:x:Selected': 'S39B:P5', 'DP:S:OrbitControlLawYSDDS_RUN': 0L,
'S26FB:bpm4:y:Selected': 'S26B:P0', 'S18FB:bpm4:y:Selected': '16',
'S9FB:bpm4:x:Selected': 'S9B:P0', 'S4FB:bpm4:y:Selected': 'S4A:P0',
'S8FB:bpm4:y:Selected': '16', 'S24FB:bpm4:x:Selected': 'S24B:P0',
'S3FB:bpm4:x:Selected': 'S3B:P0', 'S27FB:bpm2:y:Selected': 'S27A:P4',
'DP:S:OrbitControlLawXSDDS_RUN': 0L, 'S11FB:bpm4:y:Selected': '16',
'S22FB:bpm1:x:Selected': 'S22B:P5', 'S20FB:bpm2:x:Selected': 'S20B:P3',
'S14FB:bpm3:y:Selected': 'S14B:P3', 'S22FB:bpm4:y:Selected': 'S22A:P0',
'S3FB:bpm1:y:Selected': 'S3A:P4', 'S24FB:bpm1:x:Selected': 'S24B:P5',
'S37FB:bpm4:x:Selected': 'S37B:P2', 'SRFB:HPFilterEnable': 1L,
'S5FB:bpm2:y:Selected': 'S5B:P5', 'S7FB:bpm1:x:Selected': 'S7A:P2',
'S2FB:bpm3:y:Selected': 'S2B:P2', 'S15FB:bpm2:x:Selected': 'S15B:P4',
'S39FB:bpm3:y:Selected': 'S39B:P4', 'S20FB:bpm3:x:Selected': 'S20A:P0',
'S7FB:bpm4:x:Selected': '16', 'S21FB:bpm4:x:Selected': 'S21B:P0',
'DaqBurstToBroker': 0L, 'S40FB:bpm4:y:Selected': '16',
'S33FB:bpm2:y:Selected': 'S33B:P3', 'DP:LoopPeriod': 1868.7999267578125,
'S27FB:bpm3:y:Selected': 'S27B:P5', 'S18FB:bpm1:x:Selected': 'S18B:P5',
'S23FB:bpm3:x:Selected': 'S23A:P0', 'S20FB:bpm1:y:Selected': 'S20A:P3',
'S21FB:bpm4:y:Selected': 'S21B:P0', 'S9FB:bpm2:x:Selected': 'S9B:P3',
'S15FB:bpm1:y:Selected': 'S15A:P2', 'DaqUser': '',
'S33FB:bpm1:x:Selected': 'S33B:P5', 'S29FB:bpm2:y:Selected': 'S29B:P5',
'S38FB:bpm3:y:Selected': 'S38B:P3', 'S20FB:bpm3:y:Selected': 'S20B:P4',
'S13FB:bpm2:x:Selected': 'S13B:P5', 'S40FB:bpm2:x:Selected': 'S40B:P5',
'S38FB:bpm1:y:Selected': 'S38B:P5', 'S11FB:bpm1:y:Selected': 'S11B:P5',
'DaqBurstToFile': 1L, 'S10FB:bpm4:y:Selected': 'S10B:P0',
'S23FB:bpm1:x:Selected': 'S23B:P5', 'DP:S:OrbitControlLawYSDDS_SUSP':
0L, 'S28FB:bpm4:x:Selected': '16', 'S2FB:bpm2:y:Selected': 'S2B:P4',
'S26FB:bpm3:x:Selected': 'S26B:P3', 'S35FB:bpm4:y:Selected': '16',
'S25FB:bpm1:y:Selected': 'S25B:P4', 'S29FB:bpm3:x:Selected': 'S29B:P5',
'S22FB:bpm1:y:Selected': 'S22A:P2', 'S26FB:bpm3:y:Selected': 'S26B:P3',
'S2FB:bpm2:x:Selected': 'S2B:P5', 'S7FB:bpm2:y:Selected': 'S7B:P3',
'S17FB:bpm3:x:Selected': 'S17A:P0', 'S37FB:bpm4:y:Selected': 'S37B:P2',
'S1FB:bpm4:y:Selected': 'S1B:P3', 'daqId':
'5ffd2ecb-e990-4154-b36d-d24b475a3069', 'S25FB:bpm4:x:Selected':
'S25A:P0', 'S1FB:bpm2:x:Selected': 'S1B:P5', 'S32FB:bpm3:y:Selected':
'S32A:P0', 'S23FB:bpm3:y:Selected': 'S23A:P0', 'S9FB:bpm4:y:Selected':
'S9A:P0', 'DaqSddsColumnsPerId': '1,1,360,80,40',
'S14FB:bpm2:y:Selected': 'S14A:P4', 'SRFB:Kp:y': 6.0, 'SRFB:Kp:x': 28.0,
'S33FB:bpm2:x:Selected': 'S33B:P3', 'S10FB:bpm1:x:Selected': 'S10B:P5',
'S2FB:bpm4:x:Selected': 'S2B:P2', 'S38FB:bpm2:y:Selected': 'S38B:P4',
'S17FB:bpm2:x:Selected': 'S17B:P3', 'S33FB:bpm4:y:Selected': 'S33B:P0',
'S39FB:bpm1:y:Selected': 'S39A:P2', 'S21FB:bpm1:y:Selected': 'S21A:P4',
'DaqBurstFileNamePrefix': 'rtfbStream', 'S4FB:bpm4:x:Selected':
'S4B:P0', 'S36FB:bpm1:y:Selected': 'S36A:P2', 'S14FB:bpm2:x:Selected':
'S14B:P3', 'S24FB:bpm3:y:Selected': 'S24A:P0', 'S38FB:bpm4:x:Selected':
'16', 'S12FB:bpm4:y:Selected': '16', 'S1FB:bpm3:x:Selected': 'S1B:P3',
'S11FB:bpm3:y:Selected': 'S11A:P0', 'fileModificationTimestamp':
'2017/09/20 10:46:09 CDT', 'S6FB:bpm2:x:Selected': 'S6B:P2',
'S35FB:bpm2:x:Selected': 'S35B:P2', 'S8FB:bpm1:y:Selected': 'S8B:P4',
'S16FB:bpm2:y:Selected': 'S16B:P2', 'S18FB:bpm4:x:Selected': '16',
'S5FB:bpm2:x:Selected': 'S5B:P2', 'S37FB:bpm1:y:Selected': 'S37A:P2',
'S36FB:bpm4:y:Selected': 'S36B:P2', 'S9FB:bpm1:x:Selected': 'S9B:P5',
'S1FB:bpm4:x:Selected': 'S1B:P2', 'S13FB:bpm2:y:Selected': 'S13B:P4',
'S1FB:bpm3:y:Selected': 'S1B:P4', 'S12FB:bpm4:x:Selected': 'S12B:P3',
'DaqBurstDestination': 'storageService', 'S27FB:bpm3:x:Selected':
'S27B:P2', 'S21FB:bpm3:y:Selected': 'S21A:P0', 'S22FB:bpm4:x:Selected':
'S22B:P0', 'S33FB:bpm1:y:Selected': 'S33A:P3', 'S3FB:bpm2:y:Selected':
'S3B:P4', 'S40FB:bpm3:y:Selected': 'S40B:P2', 'S10FB:bpm2:y:Selected':
'S10B:P3', 'SRFB:LoopClosed:x': 0L, 'SRFB:LoopClosed:y': 0L,
'S25FB:bpm1:x:Selected': 'S25A:P4', 'SRFB:LoopPeriod':
428.6399841308594, 'S31FB:bpm3:x:Selected': 'S31A:P0',
'S38FB:bpm1:x:Selected': 'S38B:P5', 'S13FB:bpm4:y:Selected': '16',
'S13FB:bpm4:x:Selected': 'S13B:P0', 'S17FB:bpm4:y:Selected': 'S17B:P0',
'S11FB:bpm1:x:Selected': 'S11B:P5', 'S19FB:bpm1:x:Selected': 'S19A:P4',
'S39FB:bpm4:x:Selected': '16', 'S16FB:bpm4:y:Selected': 'S16B:P0',
'S16FB:bpm3:y:Selected': 'S16A:P0', 'S39FB:bpm3:x:Selected': 'S39B:P2',
'S18FB:bpm3:x:Selected': 'S18A:P0', 'S25FB:bpm4:y:Selected': '16',
'fileLocations':
[u'extrepid://apsgpfs08.xray.aps.anl.gov/gdata/dm/APSU/Demo-20170919-10/2017/09/20/rtfbStream.20170920104607001.sdds'],
'DP:DecimateFactor': 15.0, 'S6FB:bpm2:y:Selected': 'S6B:P2',
'S25FB:bpm3:x:Selected': 'S25B:P3', 'S36FB:bpm1:x:Selected': 'S36A:P2',
'DP:EnableWriteVCor2RMC': 0L, 'S31FB:bpm2:x:Selected': 'S31B:P3',
'S20FB:bpm2:y:Selected': 'S20A:P4', 'S2FB:bpm3:x:Selected': 'S2B:P3',
'S5FB:bpm1:x:Selected': 'S5B:P5', 'S23FB:bpm2:x:Selected': 'S23B:P3',
'S3FB:bpm3:x:Selected': 'S3A:P0', 'S16FB:bpm2:x:Selected': 'S16B:P2',
'S32FB:bpm2:x:Selected': 'S32A:P0', 'fileCreationTime': 1505922369,
'S19FB:bpm2:x:Selected': 'S19B:P4', 'S16FB:bpm1:y:Selected': 'S16A:P4',
'S34FB:bpm4:y:Selected': 'S34B:P2'}


itemRestApi.getItemByQrId(509)
item = itemRestApi.getItemByQrId(509)
newProperty = itemRestApi.addPropertyValueToItemWithId(item['id'],'File')
propertyRestApi.addPropertyMetadataToPropertyValue(newProperty['id'], metadataDict=var)
