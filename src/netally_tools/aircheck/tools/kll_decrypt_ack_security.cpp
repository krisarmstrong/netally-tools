// Filename: kll_decrypt_ack_security.cpp
// Revision: 6/18/2011
//
// Description:
//   C program to decrypt the security section of an AirCheck profile.
//

#if 0
 <Network>
  <SSID>64656661756C74</SSID>
  <SSIDLength>7</SSIDLength>
  <IPDHCP>true</IPDHCP>
  <Encrypted>4065029EFEACAD9F861D38FEEA36810C9F25386286F03F6B651D3CEF4F1C9720098F792B71B4BFB330B65990DA5814C4EF25EE7E1B109B8D0C34FF0E6634FB7A4F57DAE80C547165722857335095D1A0CF09432F572110B802D30366E316A200</Encrypted>
  <Security>
   <AuthenticationType>1</AuthenticationType>
   <EncryptionType>1</EncryptionType>
   <EAPType>0</EAPType>
  </Security>
 </Network>
 
<Encrypted>
40 65 02 9E FE AC AD 9F 
86 1D 38 FE EA 36 81 0C 
9F 25 38 62 86 F0 3F 6B 
65 1D 3C EF 4F 1C 97 20 
09 8F 79 2B 71 B4 BF B3 
30 B6 59 90 DA 58 14 C4 
EF 25 EE 7E 1B 10 9B 8D 
0C 34 FF 0E 66 34 FB 7A 
4F 57 DA E8 0C 54 71 65 
72 28 57 33 50 95 D1 A0 
CF 09 43 2F 57 21 10 B8 
02 D3 03 66 E3 16 A2 00
</Encrypted>
#endif

#include <stdio.h>
#include <stdlib.h>

unsigned char sampleEnc[] = {
0x40, 0x65, 0x02, 0x9E, 0xFE, 0xAC, 0xAD, 0x9F, 
0x86, 0x1D, 0x38, 0xFE, 0xEA, 0x36, 0x81, 0x0C, 
0x9F, 0x25, 0x38, 0x62, 0x86, 0xF0, 0x3F, 0x6B, 
0x65, 0x1D, 0x3C, 0xEF, 0x4F, 0x1C, 0x97, 0x20, 
0x09, 0x8F, 0x79, 0x2B, 0x71, 0xB4, 0xBF, 0xB3, 
0x30, 0xB6, 0x59, 0x90, 0xDA, 0x58, 0x14, 0xC4, 
0xEF, 0x25, 0xEE, 0x7E, 0x1B, 0x10, 0x9B, 0x8D, 
0x0C, 0x34, 0xFF, 0x0E, 0x66, 0x34, 0xFB, 0x7A, 
0x4F, 0x57, 0xDA, 0xE8, 0x0C, 0x54, 0x71, 0x65, 
0x72, 0x28, 0x57, 0x33, 0x50, 0x95, 0xD1, 0xA0, 
0xCF, 0x09, 0x43, 0x2F, 0x57, 0x21, 0x10, 0xB8, 
0x02, 0xD3, 0x03, 0x66, 0xE3, 0x16, 0xA2, 0x00
};

int sampleSize = sizeof(sampleEnc);

int main(void)
{
    printf("DEBUG> sampleSize= %d\n", sampleSize);

#if 0 
// ProfileContainer.cs Line 778
    unsafe private void InitSP()
    {
        char[] chars = { '4', 'd', '6', 'a', '5', 'a', '5', '9', '4', 'c', '5', '6', '5', '1', '3', '2', '5', '6', '6', '6', '7', '0', '4', '7', '3', '4', '5', '5', '5', '1', '6', 'd',
                         '4', '8', '7', '2', '5', '1', '6', '9', '3', '1', '7', '6', '6', '9', '7', '9', '7', '0', '7', '9', '3', '0', '5', '1', '5', '9', '4', '2', '6', '9', '3', '3' };
        fixed (char* pChars = chars)
        {
            m_passwordDefault = new System.Security.SecureString(pChars, chars.Length);
        }
        m_passwordCustom = new System.Security.SecureString();
    }

// ProfileContainer.cs Line 790
    /// Fills the encrypted xml field with data from a security xml data tree
    /// </summary>
    /// <param name="profile">Profile to place the encrypted xml field in</param>
    /// <param name="xdd">xml data document to construct the output into</param>
    /// <param name="password">Securestring password to encrypt the encrypted xml field</param>
    private void FillEncryption(WaffleProfileDS profile, System.Xml.XmlDataDocument xdd, System.Security.SecureString password)
    {
        // Create a new xml Writer settings object and configure for a memory stream
        System.Xml.XmlWriterSettings xws = new System.Xml.XmlWriterSettings();
        xws.ConformanceLevel = System.Xml.ConformanceLevel.Fragment;
        xws.Encoding = System.Text.Encoding.UTF8;
        xws.Indent = false;

        // Create a memory stream object to contain the unecrypted xml
        StringBuilder strBuilder = new StringBuilder();
        System.Xml.XmlWriter xw = System.Xml.XmlWriter.Create(strBuilder, xws);

        byte[] encrypted;
        // For each security found, encrypt it and store it in the networks encrypted block only if that encrypted block
        // doesn't already exist
        foreach (WaffleProfileDS.SecurityRow sr in profile.Security)
        {
            // If the encrypted block does not exist for this network
            if (sr.NetworkRow.IsEncryptedNull() || sr.NetworkRow.Encrypted.Length == 0)
            {
                // Write the XML to the memory stream
                xdd.GetElementFromRow(sr).WriteContentTo(xw);
                xw.Flush();
                // Encrypt the memory stream using AES
                if (ProfileIO.EncryptAES(ProfileIO.GetByteArrayFromString(strBuilder.ToString()), password, out encrypted))
                {
                    // Write the ascii hex values out to the encrypted xml node
                    /////// BASE64           sr.NetworkRow.Encrypted = Convert.ToBase64String(ProfileIO.GetByteArrayfromHexValues(encryptedString));
                    sr.NetworkRow.Encrypted = ProfileIO.GetStringFromByteArray(encrypted);
                }
                // Clear the string and strBuilder
                encrypted = null;
                strBuilder.Length = 0;
            }
        }
        xw.Close();
    }

// ProfileContainer.cs Line 641
    FillEncryption(profileCopy, xdd, m_passwordDefault);
#endif

#if 0
// ProfileIO.cs
using System;
using System.Collections.Generic;
using System.Diagnostics;
using System.IO;
using System.Runtime.InteropServices;
using System.Security;
using System.Security.Cryptography;
using System.Text;
using System.Text.RegularExpressions;

namespace ToolLibWc
{
    /// <summary>
    /// Static class which provides various profile data interpretation methods
    /// </summary>
    public class ProfileIO
    {
        /// <summary>
        /// Takes in a WPA password and SSID (salt) and produces a encoded Pre-shared key 40 bytes long (first 32 = psk)
        /// </summary>
        /// <param name="password">WPA password to encode, must be between 8 and 63 characters long</param>
        /// <param name="ssid">SSID to use for the encoding</param>
        /// <param name="ssidlength">length of the SSID being used</param>
        /// <param name="output">A pointer to 40 bytes of allocated memory to place the result</param>
        /// <returns>returns 0 if the input paramters were not the correct length, returns 1 if success </returns>
        [DllImport("WPApskUtil.dll", SetLastError = true)]
        protected static extern int PasswordHash_PBKDF2(
            [MarshalAs(UnmanagedType.LPStr)] 
            string password,
            [MarshalAs(UnmanagedType.LPStr)] 
            string ssid,
            int ssidlength,
            IntPtr output);

        // strings read in/out from the ACL files
        private const string ACL_UNAUTHORIZED = "unauthorized";
        private const string ACL_AUTHORIZED = "authorized";
        private const string ACL_NEIGHBOR = "neighbor";
        private const string ACL_GUEST = "guest";
        private const string ACL_FLAGGED = "flagged";

        public static readonly byte[] CERTIFICATE_EMPTY = { 0, 0, 0, 0, 0, 0, 0, 0 };

        /// <summary>
        /// Encryptes an input byte array using AES 256bit secure string key.  Returns true if encryption completed with
        /// success, false otherwise.
        /// </summary>
        /// <param name="inputData">input data to encrypt</param>
        /// <param name="passKey">secureString to be used to encrypt the input data, string of hex values</param>
        /// <param name="encrypted">output encrypted data</param>
        /// <returns>true if success, false otherwise</returns>
        public static bool EncryptAES(byte[] inputData, SecureString passKey, out byte[] encrypted)
        {
            encrypted = new byte[0];

            try
            {
                // Streams required to encrypt
                MemoryStream memStream = null;

                // Create Rijndael AES object
                using (var aesRijndael = new RijndaelManaged())
                {
                    aesRijndael.BlockSize = 128;
                    aesRijndael.KeySize = 256;
                    aesRijndael.Key = GetByteArrayfromHexValues(GetStringfromSecureString(passKey));
                    aesRijndael.Padding = PaddingMode.Zeros;
                    aesRijndael.Mode = CipherMode.ECB;

                    var encryptor = aesRijndael.CreateEncryptor(aesRijndael.Key, aesRijndael.IV);

                    memStream = new MemoryStream();
                    using (CryptoStream cryptStream = new CryptoStream(memStream, encryptor, CryptoStreamMode.Write))
                    {
                        cryptStream.Write(inputData, 0, inputData.Length);
                        cryptStream.FlushFinalBlock();
                        cryptStream.Close();
                    }
                    aesRijndael.Clear();
                }
                memStream.Close();

                encrypted = memStream.ToArray();
                return true;
            }
            catch (Exception ex1)
            {
                Debug.WriteLine(ex1.ToString());
                return false; // if any errors occured, return false
            }
        }

        /// <summary>
        /// Uses a Rijndael AES managed object to decrypt a byte stream.
        /// </summary>
        /// <param name="inputData">encrypted byte stream to decrypte</param>
        /// <param name="passKey">secure string password to decrypte the encrypted byte array</param>
        /// <param name="decrypted">output decrypted byte array of the input</param>
        /// <returns>returns true if the decryption process completed without failure/exception, false otherwise</returns>
        public static bool DecryptAES(byte[] inputData, SecureString passKey, out byte[] decrypted)
        {
            decrypted = new byte[inputData.Length];

            try
            {
                // Streams required to encrypt
                MemoryStream memStream = null;

                // Create Rijndael AES object
                using (var aesRijndael = new RijndaelManaged())
                {
                    aesRijndael.BlockSize = 128;
                    aesRijndael.KeySize = 256;
                    aesRijndael.Key = GetByteArrayfromHexValues(ProfileIO.GetStringfromSecureString(passKey));
                    aesRijndael.Padding = PaddingMode.Zeros;
                    aesRijndael.Mode = CipherMode.ECB;

                    var decryptor = aesRijndael.CreateDecryptor(aesRijndael.Key, aesRijndael.IV);

                    memStream = new MemoryStream(inputData);

                    using (var cryptStream = new CryptoStream(memStream, decryptor, CryptoStreamMode.Read))
                    {
                        cryptStream.Read(decrypted, 0, inputData.Length);
                        cryptStream.Close();
                    }
                    aesRijndael.Clear();
                }
                memStream.Close();
                return true;
            }
            catch (Exception ex1)
            {
                Debug.WriteLine(ex1.ToString());
                return false; // if any errors occured, return false
            }
        }

#endif

#if 0
// Legacy C# sample illustrating how the original tooling invoked AES routines.
// Retained for reference only; not valid C++.

byte sampleEnc[] = {
0x40, 0x65, 0x02, 0x9E, 0xFE, 0xAC, 0xAD, 0x9F,
0x86, 0x1D, 0x38, 0xFE, 0xEA, 0x36, 0x81, 0x0C,
0x9F, 0x25, 0x38, 0x62, 0x86, 0xF0, 0x3F, 0x6B,
0x65, 0x1D, 0x3C, 0xEF, 0x4F, 0x1C, 0x97, 0x20,
0x09, 0x8F, 0x79, 0x2B, 0x71, 0xB4, 0xBF, 0xB3,
0x30, 0xB6, 0x59, 0x90, 0xDA, 0x58, 0x14, 0xC4,
0xEF, 0x25, 0xEE, 0x7E, 0x1B, 0x10, 0x9B, 0x8D,
0x0C, 0x34, 0xFF, 0x0E, 0x66, 0x34, 0xFB, 0x7A,
0x4F, 0x57, 0xDA, 0xE8, 0x0C, 0x54, 0x71, 0x65,
0x72, 0x28, 0x57, 0x33, 0x50, 0x95, 0xD1, 0xA0,
0xCF, 0x09, 0x43, 0x2F, 0x57, 0x21, 0x10, 0xB8,
0x02, 0xD3, 0x03, 0x66, 0xE3, 0x16, 0xA2, 0x00
};

char[] chars = { /* omitted for brevity */ };
fixed (char* pChars = chars)
{
    m_passwordDefault = new System.Security.SecureString(pChars, chars.Length);
}
ProfileIO.DecryptAES(sampleEnc, password, out decrypted))
string s = ProfileIO.GetStringFromByteArray(decrypted);

Console.WriteLine(s);
#endif
    
    return 0;
}
