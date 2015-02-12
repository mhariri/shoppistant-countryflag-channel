import json
import datetime
import logging

import webapp2

from mapping import mappings


PLUGIN_INFO = {
    "name": "Product country flag"
}

# cache for 2 days
EXPIRATION_IN_SECONDS = 2 * 24 * 60 * 60


class GMT(datetime.tzinfo):
    def utcoffset(self, dt):
        return datetime.timedelta(hours=10)

    def tzname(self, dt):
        return "GMT"

    def dst(self, dt):
        return datetime.timedelta(0)


def get_expiration_stamp(seconds):
    gmt = GMT()
    delta = datetime.timedelta(seconds=seconds)
    expiration = datetime.datetime.now()
    expiration = expiration.replace(tzinfo=gmt)
    expiration = expiration + delta
    return expiration.strftime("%a, %d %b %Y %H:%M:%S %Z")


class CountryMappingNotFound(Exception):
    pass


def find_mapping(prefix):
    for m in mappings:
        if prefix >= m[0] and prefix <= m[1]:
            return (m[3], "flags/flags_iso/32/%s.png" % m[2])
    raise CountryMappingNotFound()


class MainHandler(webapp2.RequestHandler):
    def get(self):
        self.set_default_headers()

        barcode = self.request.params.get("q", None)
        if barcode:

            open_details = self.request.params.get("d", None)
            if open_details:
                self.redirect("http://www.gs1.org/company-prefix")
            else:
                try:
                    prefix = barcode[0:3]
                    (country, flag) = find_mapping(prefix)
                    self.send_rating_image(country, flag)
                except CountryMappingNotFound:
                    # amazon sometimes blocks the request,
                    # just log and ignore it silently
                    error = "No country mapping found for: " + str(prefix)
                    logging.error(error)
                    self.response.write(error + "\n")
                    self.response.status = 404

        else:
            self.response.content_type = "application/json"
            self.response.write(json.dumps(PLUGIN_INFO))

    def set_default_headers(self):
        # allow CORS
        self.response.headers.add_header("Access-Control-Allow-Origin", "*")
        self.response.headers["Expires"] = get_expiration_stamp(EXPIRATION_IN_SECONDS)
        self.response.headers["Content-Type"] = "application/json"
        self.response.headers["Cache-Control"] = "public, max-age=%d" % EXPIRATION_IN_SECONDS

    def send_rating_image(self, country, flag):
        self.response.content_type = "image/png"
        self.response.body_file = open(flag)


app = webapp2.WSGIApplication([
                                  ('/', MainHandler)
                              ], debug=True)
