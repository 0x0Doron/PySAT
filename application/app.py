#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from flask import Flask, render_template, redirect, url_for, request
from flask_socketio import SocketIO, send, emit

from modules.anon import anon_proxy
from modules.anon.anon_proxy import CustomProxy

from modules.crypto import crypto_utilities

from modules.forensics import image_utilities
from modules.forensics.image_utilities import CustomImage

from modules.scanner import web
from modules.scanner import server_scanner

import controller

import re
import os


app = Flask(__name__)
app.config['SECRET KEY'] = 'secret!'
app.config['DEBUG'] = True
socketio = SocketIO(app)



@app.route('/')
def index():
    if controller.any_proxy():
        proxy = controller.get_current_proxy()
        ip = proxy.ip
    else:
        ip = controller.get_real_ip()
        proxy=None

    return render_template('index.html', ip=ip, proxy=proxy)


####################################################################
##################### ANONYMOUS IP #################################
####################################################################

@app.route('/reset_ip')
def reset_ip():
    controller.remove_proxy()
    return redirect(url_for('index'))


@app.route('/anon')
def anon():
    proxies = anon_proxy.get_proxy_list()
    proxies = proxies#[:50]

    return render_template('anon/anon.html', nproxies=len(proxies), proxies=proxies, cproxy=None) # cproxy -> config.txt defined proxy (customproxy)


@app.route('/anon/set_proxy/<string:ip>/<string:port>/<string:country>/<string:anonymous>', methods=['GET', 'POST'])
@app.route('/anon/set_proxy', methods=['GET', 'POST'])
def set_proxy(ip=None, port=None, country=None, anonymous=None):

    if request.method == 'POST':
        proxy_addr = request.form['proxyAddr']

        if controller.is_ip_port(proxy_addr):

            ip = proxy_addr.split(':')[0]
            port = proxy_addr.split(':')[1]
            proxy = CustomProxy(ip, port, 'unkwon', 'unkwon')
        else:
            return redirect(url_for('anon'))
    else:
        proxy = CustomProxy(ip, port, country, anonymous)

    proxy_works = controller.test_proxy_connection(proxy)

    if proxy_works:
        controller.config_proxy(proxy)    # init proxy.txt
        return redirect(url_for('index'))
    return redirect(url_for('anon'))

####################################################################
##################### NETWORKING ###################################
####################################################################

@app.route('/networking')
def networking():
    return render_template('networking/networking.html')


####################################################################
##################### CRYPTOGRAPHY #################################
####################################################################


@app.route('/crypto')
def crypto():

    hash_types = crypto_utilities.get_hash_types()
    encodings = crypto_utilities.get_encodings()
    decoders = crypto_utilities.get_decoders()

    return render_template('crypto/crypto.html', hash_types=hash_types, encodings=encodings, decoders=decoders)


@socketio.on('hash identify')
def handle_hash_check(hash):
    identifier = crypto_utilities.hash_identifier(hash)

    if identifier:
        result = ', '.join(identifier)

    else:
        result = 'Match not found :('
    emit('hash identify', result)


@socketio.on('text to hash')
def handle_text_to_hash(text_hash):
    text = text_hash.split('[flag]')[0]
    type = text_hash.split('[flag]')[1]
    hash = crypto_utilities.text_to_hash(text, type)

    if hash is not None:
        result = hash
    else:
        result = 'Error'
    emit('text to hash', result)


@socketio.on('text to encode')
def handle_text_to_encode(text_encoder):
    text = text_encoder.split('[flag]')[0]
    encoder = text_encoder.split('[flag]')[1]

    code = crypto_utilities.text_to_encode(text, encoder)

    emit('text to encode', code)


@socketio.on('decode code')
def handle_text_to_encode(code_decoder):
    code = code_decoder.split('[flag]')[0]
    decoder = code_decoder.split('[flag]')[1]
    text = crypto_utilities.decode_code(code, decoder)
    print(text)
    if text is None:
        text = 'Unable to decode...'

    emit('decode code', text)


####################################################################
##################### FORENSICS ####################################
####################################################################

@app.route('/forensics')
@app.route('/forensics/pdfs')
@app.route('/forensics/virus')
def forensics():
    template = 'forensics/forensics.html'
    if 'pdfs' in request.path:
        template = 'forensics/pdfs.html'

    elif 'virus' in request.path:
        template = 'forensics/virus.html'

    return render_template(template)


@app.route('/forensics/images')
@app.route('/forensics/images/<id>')
def forensics_images(id=None):
    images_tuple = controller.get_images()  # list of images (image_name, full_path)
    images_name = images_tuple[0]
    images_path = images_tuple[1]

    images_to_exif = []
    size = len(images_path)

    for i in range(size):
        image_to_exif = CustomImage(images_name[i], images_path[i])

        if image_to_exif.exif and image_to_exif is not None:
            images_to_exif.append(image_to_exif)

    if id is None:

        return render_template('forensics/images.html', images=images_to_exif, size=size)

    image = images_to_exif[int(id)]

    return render_template('forensics/image.html', image=image, id=id)  # Specific image



####################################################################
##################### SCANNER ######################################
####################################################################

@app.route('/scanner')
def scanner():
    return render_template('scanner/scanner.html')

####################################################################
##################### SERVER SCANNER ###############################
####################################################################


@app.route('/scanner/server')
def port_scanner():

    anon = False
    if controller.any_proxy():
        anon = True

    return render_template('scanner/servers.html', anon=anon)


@socketio.on('scan server')
def scan_server(host):
    scanner_data = controller.parse_server_scanner_data(host)
    if scanner_data is not None:

        scan_info = server_scanner.load_port_scanner(scanner_data[1], scanner_data[2], scanner_data[3], scanner_data[4])

        threads = str(scan_info['threads'])
        ports_list = scan_info['ports']
        time = str(scan_info['time'])
        banner_list = scan_info['banner']

        # port parse

        ports = ''

        for port in ports_list:
            if ports != '':
                ports += ':'+str(port)
            else:
                ports += str(port)



        port_banner = [ports_list[i]+'[banner]'+banner_list[i] for i in range(len(ports_list))]

        port_banner_data = ''

        for pb in port_banner:
            if port_banner_data != '':
                port_banner_data += '[flag]'+str(pb)
            else:
                 port_banner_data += str(pb)

        # data sendinf via sockets

        emit('time', time)
        emit('threads', threads)
        emit('banner', port_banner_data)

        # 4 ip geolocation info and map displaying

        if scanner_data[0] == 'ipgps':
            lat_long = server_scanner.get_gps(scanner_data[1])
            data = str(lat_long[0])+':'+str(lat_long[1])
            emit('ipgps', data)
            print(data)
        else:
            pass


    else:
        emit('scan server', 'Target Error: worng input format.')

####################################################################
##################### WEB SCANNER ##################################
####################################################################


@app.route('/scanner/web')
def web_scanner():
    anon = False
    if controller.any_proxy():
        anon = True
    username = controller.get_pc_user()

    return render_template('scanner/web.html', username=username, anon=anon)


@socketio.on('scan web')
def scan_web(param):
    params = param.split(':')   # carefull with the http/s <:>

    controller.load_web_scanner(params)




####################################################################
##################### HELP #########################################
####################################################################


@app.route('/help')
def help():
    return render_template('help/help.html')



@app.errorhandler(404)
def page_not_found(error):
    return render_template('page_not_found.html', error=error)



if __name__ == '__main__':
    socketio.run(app)
