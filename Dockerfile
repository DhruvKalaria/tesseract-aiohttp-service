FROM python:3.6.6-alpine3.8
LABEL maintainer="Dhruv Kalaria:dhruvkalaria@gmail.com"

ENV TINI_VERSION=v0.18.0
ENV SHELL=/bin/bash
ENV CC /usr/bin/clang
ENV CXX /usr/bin/clang++
ENV LANG=C.UTF-8
ENV TESSDATA_PREFIX=/usr/local/share/tessdata


# Installing dev tools
WORKDIR /tmp
RUN apk update && apk upgrade \
    && apk add --no-cache openssl openssl-dev bash tini leptonica-dev openjpeg-dev tiff-dev libpng-dev zlib-dev libgcc \
    mupdf-dev jbig2dec-dev freetype-dev openblas-dev ffmpeg-dev jasper-dev linux-headers \
    enchant-dev aspell-dev aspell-en \
    && apk add --no-cache --virtual .dev-deps git clang clang-dev g++ make automake autoconf libtool pkgconfig \
    cmake ninja \
    && apk add --no-cache --virtual .dev-testing-deps -X http://dl-3.alpinelinux.org/alpine/edge/testing \
    autoconf-archive \
    && ln -s /usr/include/locale.h /usr/include/xlocale.h

# Install Tesseract 4.0 from master
RUN mkdir /usr/local/share/tessdata \
    && mkdir src \
    && cd src \
    && wget https://github.com/tesseract-ocr/tessdata_fast/raw/master/eng.traineddata -P /usr/local/share/tessdata \
    && git clone --depth 1 https://github.com/tesseract-ocr/tesseract.git \
    && cd tesseract \
    && ./autogen.sh \
    && ./configure --build=x86_64-alpine-linux-musl --host=x86_64-alpine-linux-musl \
    && make \
    && make install \
    && cd /tmp/src

# Install python pacakges
RUN pip install --no-cache-dir --upgrade uvloop==0.11.2 aiohttp==3.4.4 gunicorn==19.9.0 Pillow==5.2.0 imutils==0.4.6 pdf2image==0.1.14 pyocr==0.5.3

# Post install cleanup
RUN find /usr/local \
    \( -type d -a -name test -o -name tests \) \
    -o \( -type f -a -name '*.pyc' -o -name '*.pyo' \) \
    -exec rm -rf '{}' + \
    && runDeps="$( \
    scanelf --needed --nobanner --recursive /usr/local \
    | awk '{ gsub(/,/, "\nso:", $2); print "so:" $2 }' \
    | sort -u \
    | xargs -r apk info --installed \
    | sort -u \
    )" \
    && apk add --virtual .python-rundeps $runDeps \
    && apk del .dev-deps .dev-testing-deps .python-rundeps \
    && cd /tmp \
    && rm -rf /var/cache/apk/* \
    && rm -rf /tmp/src

ADD service /srv/ocr-processor/current/service
ADD server.py /srv/ocr-processor/current/
WORKDIR /srv/ocr-processor/current/
RUN mkdir log && mkdir temp
ENTRYPOINT [ "/sbin/tini", "--" ]
EXPOSE 8000
CMD [ "/bin/bash", "-c", "gunicorn server:app --bind :8000 --worker-class aiohttp.GunicornUVLoopWebWorker" ]