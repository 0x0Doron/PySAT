#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#
#   Bunch of modules for different cryptographic utilities
#

import re
import hashlib
import codecs
import base64

# REGEX FOR DIFFERENT HASHESH

hashes_regex = (
("Blowfish(Eggdrop)", r"^\+[a-zA-Z0-9\/\.]{12}$"),
("Blowfish(OpenBSD)", r"^\$2a\$[0-9]{0,2}?\$[a-zA-Z0-9\/\.]{53}$"),
("Blowfish crypt", r"^\$2[axy]{0,1}\$[a-zA-Z0-9./]{8}\$[a-zA-Z0-9./]{1,}$"),
("DES(Unix)", r"^.{0,2}[a-zA-Z0-9\/\.]{11}$"),
("MD5(Unix)", r"^\$1\$.{0,8}\$[a-zA-Z0-9\/\.]{22}$"),
("MD5(APR)", r"^\$apr1\$.{0,8}\$[a-zA-Z0-9\/\.]{22}$"),
("MD5(MyBB)", r"^[a-fA-F0-9]{32}:[a-z0-9]{8}$"),
("MD5(ZipMonster)", r"^[a-fA-F0-9]{32}$"),
("MD5 crypt", r"^\$1\$[a-zA-Z0-9./]{8}\$[a-zA-Z0-9./]{1,}$"),
("MD5 apache crypt", r"^\$apr1\$[a-zA-Z0-9./]{8}\$[a-zA-Z0-9./]{1,}$"),
("MD5(Joomla)", r"^[a-fA-F0-9]{32}:[a-zA-Z0-9]{16,32}$"),
("MD5(Wordpress)", r"^\$P\$[a-zA-Z0-9\/\.]{31}$"),
("MD5(phpBB3)", r"^\$H\$[a-zA-Z0-9\/\.]{31}$"),
("MD5(Cisco PIX)", r"^[a-zA-Z0-9\/\.]{16}$"),
("MD5(osCommerce)", r"^[a-fA-F0-9]{32}:[a-zA-Z0-9]{2}$"),
("MD5(Palshop)", r"^[a-fA-F0-9]{51}$"),
("MD5(IP.Board)", r"^[a-fA-F0-9]{32}:.{5}$"),
("MD5(Chap)", r"^[a-fA-F0-9]{32}:[0-9]{32}:[a-fA-F0-9]{2}$"),
("Juniper Netscreen/SSG (ScreenOS)", r"^[a-zA-Z0-9]{30}:[a-zA-Z0-9]{4,}$"),
("Fortigate (FortiOS)", r"^[a-fA-F0-9]{47}$"),
("Minecraft(Authme)", r"^\$sha\$[a-zA-Z0-9]{0,16}\$[a-fA-F0-9]{64}$"),
("Lotus Domino", r"^\(?[a-zA-Z0-9\+\/]{20}\)?$"),
("Lineage II C4", r"^0x[a-fA-F0-9]{32}$"),
("CRC-96(ZIP)", r"^[a-fA-F0-9]{24}$"),
("NT crypt", r"^\$3\$[a-zA-Z0-9./]{8}\$[a-zA-Z0-9./]{1,}$"),
("Skein-1024", r"^[a-fA-F0-9]{256}$"),
("RIPEMD-320", r"^[A-Fa-f0-9]{80}$"),
("EPi hash", r"^0x[A-F0-9]{60}$"),
("EPiServer 6.x < v4", r"^\$episerver\$\*0\*[a-zA-Z0-9]{22}==\*[a-zA-Z0-9\+]{27}$"),
("EPiServer 6.x >= v4", r"^\$episerver\$\*1\*[a-zA-Z0-9]{22}==\*[a-zA-Z0-9]{43}$"),
("Cisco IOS SHA256", r"^[a-zA-Z0-9]{43}$"),
("SHA-1(Django)", r"^sha1\$.{0,32}\$[a-fA-F0-9]{40}$"),
("SHA-1 crypt", r"^\$4\$[a-zA-Z0-9./]{8}\$[a-zA-Z0-9./]{1,}$"),
("SHA-1(Hex)", r"^[a-fA-F0-9]{40}$"),
("SHA-1(LDAP) Base64", r"^\{SHA\}[a-zA-Z0-9+/]{27}=$"),
("SHA-1(LDAP) Base64 + salt", r"^\{SSHA\}[a-zA-Z0-9+/]{28,}[=]{0,3}$"),
("SHA-512(Drupal)", r"^\$S\$[a-zA-Z0-9\/\.]{52}$"),
("SHA-512 crypt", r"^\$6\$[a-zA-Z0-9./]{8}\$[a-zA-Z0-9./]{1,}$"),
("SHA-256(Django)", r"^sha256\$.{0,32}\$[a-fA-F0-9]{64}$"),
("SHA-256 crypt", r"^\$5\$[a-zA-Z0-9./]{8}\$[a-zA-Z0-9./]{1,}$"),
("SHA-384(Django)", r"^sha384\$.{0,32}\$[a-fA-F0-9]{96}$"),
("SHA-256(Unix)", r"^\$5\$.{0,22}\$[a-zA-Z0-9\/\.]{43,69}$"),
("SHA-512(Unix)", r"^\$6\$.{0,22}\$[a-zA-Z0-9\/\.]{86}$"),
("SHA-384", r"^[a-fA-F0-9]{96}$"),
("SHA-512", r"^[a-fA-F0-9]{128}$"),
("SSHA-1", r"^({SSHA})?[a-zA-Z0-9\+\/]{32,38}?(==)?$"),
("SSHA-1(Base64)", r"^\{SSHA\}[a-zA-Z0-9]{32,38}?(==)?$"),
("SSHA-512(Base64)", r"^\{SSHA512\}[a-zA-Z0-9+]{96}$"),
("Oracle 11g", r"^S:[A-Z0-9]{60}$"),
("SMF >= v1.1", r"^[a-fA-F0-9]{40}:[0-9]{8}&"),
("MySQL 5.x", r"^\*[a-f0-9]{40}$"),
("MySQL 3.x", r"^[a-fA-F0-9]{16}$"),
("OSX v10.7", r"^[a-fA-F0-9]{136}$"),
("OSX v10.8", r"^\$ml\$[a-fA-F0-9$]{199}$"),
("SAM(LM_Hash:NT_Hash)", r"^[a-fA-F0-9]{32}:[a-fA-F0-9]{32}$"),
("MSSQL(2000)", r"^0x0100[a-f0-9]{0,8}?[a-f0-9]{80}$"),
("MSSQL(2005)", r"^0x0100[a-f0-9]{0,8}?[a-f0-9]{40}$"),
("MSSQL(2012)", r"^0x02[a-f0-9]{0,10}?[a-f0-9]{128}$"),
("TIGER-160(HMAC)", r"^[a-f0-9]{40}$"),
("SHA-256", r"^[a-fA-F0-9]{64}$"),
("SHA-1(Oracle)", r"^[a-fA-F0-9]{48}$"),
("SHA-224", r"^[a-fA-F0-9]{56}$"),
("Adler32", r"^[a-f0-9]{8}$"),
("CRC-16-CCITT", r"^[a-fA-F0-9]{4}$"),
("NTLM)", r"^[0-9A-Fa-f]{32}$"),
)


hash_types = (
'MD5',
'SHA1',
'SHA256',
'SHA512',
)

encodings = (
 "idna",
 "oem",
 "palmos",
 "punycode",
 "raw_unicode_escape",
 "rot_13",
 "undefined",
 "unicode_escape",
 "unicode_internal",
 "base64_codec",
 "bz2_codec",
 "hex_codec",
 "quopri_codec",
 "uu_codec",
 "zlib_codec",
)

decoders = (
'base64',

)

def base64_to_string(b):
    try:
        return base64.b64decode(b).decode('utf-8')
    except:
        return 'Unable to decode'


def get_hash_types():
    return hash_types

def get_encodings():
    return encodings


def get_decoders():
    return decoders


def text_to_encode(text, type):
    if 'codec' in type:
        code = codecs.encode(text.encode('utf-8'), type)
    else:
        code = codecs.encode(text, type)

    try:
        code = code.decode('ascii')
    except:
        try:
            code = code.decode('utf-8')
        except:
            return code

    return code



def decode_code(code, type):
    text = None
    if type == 'base64':
        text = base64_to_string(code)

    return text



def hash_identifier(hash):
    '''
        - Parameter: hash code
        - Return: hash type if match found or none if not found
    '''

    found_hashes = []

    for h in hashes_regex:

        try:
            is_hash = re.finditer(h[1], hash)
            matched = [match.group(0) for match in is_hash]

            if matched:
                found_hashes.append(h[0])
        except:
            pass

    if found_hashes:
        return found_hashes
    return None


def text_to_hash(text, hash_type):

    hash = None
    text = text.encode('utf-8')

    if hash_type == 'MD5':
        hash = hashlib.md5(text).hexdigest()
    elif hash_type == 'SHA1':
        hash = hashlib.sha1(text).hexdigest()
    elif hash_type == 'SHA256':
        hash = hashlib.sha256(text).hexdigest()
    elif hash_type == 'SHA512':
        hash = hashlib.sha512(text).hexdigest()

    return hash
