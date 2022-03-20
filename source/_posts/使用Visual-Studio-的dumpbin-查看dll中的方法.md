---
title: 使用Visual-Studio-的dumpbin-查看dll中的方法.md
top: false
cover: false
toc: true
mathjax: true
date: 2022-03-20 18:16:49
password:
summary:
tags: windows
categories: windows
---
---
title: 使用Visual-Studio-的dumpbin-查看dll中的方法.md
top: false
cover: false
toc: true
mathjax: true
date: 2022-03-20 18:16:49
password:
summary:
tags: windows
categories: windows
---
先进入D:\Visual Studio\VC\Tools\MSVC\14.25.28610\bin\Hostx64\x64\dumpbin.exe文件夹内部
使用dumpbin 命令即可

>dumpbin /exports C:\Users\yinkai\Desktop\XTXAppCOM_x64.dll

~~~
D:\Visual Studio\VC\Tools\MSVC\14.25.28610\bin\Hostx64\x64>dumpbin /exports C:\Users\yinkai\Desktop\XTXAppCOM_x64.dll
Microsoft (R) COFF/PE Dumper Version 14.25.28614.0
Copyright (C) Microsoft Corporation.  All rights reserved.


Dump of file C:\Users\yinkai\Desktop\XTXAppCOM_x64.dll

File Type: DLL

  Section contains the following exports for XTXAppCOM_x64.dll

    00000000 characteristics
    5B960820 time date stamp Mon Sep 10 13:58:56 2018
        0.00 version
           1 ordinal base
         110 number of functions
         110 number of names

    ordinal hint RVA      name

          2    0 000F6834 AnySign_DestoryKeyPair
          3    1 000F485C AnySign_GenKeyPair
          4    2 000F50F4 AnySign_GenPkcs10
          5    3 000F6F04 AnySign_GetTimeStampInfo
          6    4 000F57CC AnySign_SignData
          7    5 000F7368 AnySign_SignHashData
          8    6 000F5E4C AnySign_SignPkcs7Data
          9    7 000F6B04 AnySign_VerifyTimeStamp
         10    8 000EE9E0 Base64EncodeFile
         11    9 000EA3E4 ChangeAdminPass
         12    A 000F184C CheckSoftDeviceEnv
         13    B 000EED74 CreateSoftDevice
         14    C 000EC964 DeleteContainer
         15    D 000EE600 DeleteOldContainer
         16    E 000EF090 DeleteSoftDevice
         17    F 0003A024 DllCanUnloadNow
         18   10 0003A048 DllGetClassObject
         19   11 0003A338 DllInstall
         20   12 0003A184 DllRegisterServer
         21   13 0003A298 DllUnregisterServer
         22   14 000EF2CC EnableSoftDevice
         23   15 000F2E50 EnumFilesInDevice
         24   16 000ECBE0 ExportPKCS10
         25   17 000EAC64 ExportPubKey
         26   18 000E12C0 FreeUserInfo
         27   19 000EA994 GenerateKeyPair
         28   1A 000E994C GetAllDeviceSN
         29   1B 000F2100 GetAllDeviceSNEx
         30   1C 000EDE74 GetContainerCount
         31   1D 000E982C GetDeviceCount
         32   1E 000F1D1C GetDeviceCountEx
         33   1F 000EA044 GetDeviceInfo
         34   20 000E9D64 GetDeviceSNByIndex
         35   21 000ED534 GetENVSN
         36   22 000EB3F8 ImportEncCert
         37   23 000F1094 ImportKeyCertToSoftDevice
         38   24 000F1974 ImportPfxToDevice
         39   25 000EB0CC ImportSignCert
         40   26 000ED0D0 InitDevice
         41   27 000ED100 InitDeviceEx
         42   28 000EC5D0 IsContainerExist
         43   29 000EDB44 IsDeviceExist
         44   2A 000F2A2C OTP_GetChallengeCode
         45   2B 000F2888 OpenSpecifiedFolder
         46   2C 000E8548 SOF_Base64Decode
         47   2D 000E816C SOF_Base64Encode
         48   2E 000E230C SOF_ChangePassWd
         49   2F 000E48D0 SOF_DecryptData
         50   30 000E3E68 SOF_EncryptData
         51   31 000E439C SOF_EncryptDataEx
         52   32 000E190C SOF_ExportExChangeUserCert
         53   33 000E14CC SOF_ExportUserCert
         54   34 000DFF84 SOF_Finalize
         55   35 000E6184 SOF_GenRandom
         56   36 000EE10C SOF_GetAllContainerName
         57   37 000F07C8 SOF_GetCertEntity
         58   38 000E25E4 SOF_GetCertInfo
         59   39 000E29D0 SOF_GetCertInfoByOid
         60   3A 000E06A4 SOF_GetEncryptMethod
         61   3B 000E5D78 SOF_GetInfoFromSignedMessage
         62   3C 000E6E78 SOF_GetLastErrMsg
         63   3D 000E6D58 SOF_GetLastError
         64   3E 000E2114 SOF_GetPinRetryCount
         65   3F 000E041C SOF_GetSignMethod
         66   40 000E07BC SOF_GetUserList
         67   41 000E0BF4 SOF_GetUserListEx
         68   42 000E0108 SOF_GetVersion
         69   43 000F0B98 SOF_HMAC
         70   44 000E8970 SOF_HashData
         71   45 000E901C SOF_HashFile
         72   46 000DFB0C SOF_Initialize
         73   47 000DFB18 SOF_InitializeEx
         74   48 000E1EB4 SOF_Login
         75   49 000E9688 SOF_Logout
         76   4A 000E68C8 SOF_PriKeyDecrypt
         77   4B 000E63D8 SOF_PubKeyEncrypt
         78   4C 000EB860 SOF_ReadFile
         79   4D 000F1468 SOF_SelectFile
         80   4E 000E0534 SOF_SetEncryptMethod
         81   4F 000E02B0 SOF_SetSignMethod
         82   50 000E2E2C SOF_SignData
         83   51 000E3680 SOF_SignFile
         84   52 000EFF60 SOF_SignHashData
         85   53 000E52C8 SOF_SignHashMessage
         86   54 000E5290 SOF_SignMessage
         87   55 000E4DA4 SOF_SignMessageEx
         88   56 000E75F0 SOF_SymDecryptData
         89   57 000E7E44 SOF_SymDecryptFile
         90   58 000E70C4 SOF_SymEncryptData
         91   59 000E7B1C SOF_SymEncryptFile
         92   5A 000F3AA8 SOF_TSCompareNonce
         93   5B 000F3D60 SOF_TSGenPDFSignature
         94   5C 000F3310 SOF_TSGenREQ
         95   5D 000F4450 SOF_TSGetPDFSignatureInfo
         96   5E 000F4248 SOF_TSVerifyPDFSignature
         97   5F 000F2698 SOF_UpdateCert
         98   60 000E1CB0 SOF_ValidateCert
         99   61 000E3300 SOF_VerifySignedData
        100   62 000E3B14 SOF_VerifySignedFile
        101   63 000F0440 SOF_VerifySignedHashData
        102   64 000E5AB0 SOF_VerifySignedHashMessage
        103   65 000E57B8 SOF_VerifySignedMessage
        104   66 000EBCA4 SOF_WriteFile
        105   67 000EC138 SOF_WriteFileEx
        106   68 000ED8C8 SetENVSN
        107   69 000EFC08 SetUserConfig
        108   6A 000EF410 SoftDeviceBackup
        109   6B 000EF85C SoftDeviceRestore
        110   6C 000EA6BC UnlockUserPass
          1   6D 000281B8 UnlockUserPassEx

  Summary

       26000 .data
       37000 .pdata
       DA000 .rdata
        A000 .reloc
        B000 .rsrc
      2AC000 .text
~~~


