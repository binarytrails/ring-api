#!/usr/bin/env python3

import unittest, requests, json

def print_json(data):
    print(json.dumps(data, sort_keys=True, indent=4))

class TestAccount(unittest.TestCase):

    def test_accounts_get(self):
        print("\nGET /accounts/")

        res = requests.get('http://localhost:8080/accounts/')
        res = res.json()
         
        self.assertTrue('status' in res)
        self.assertEqual(res['status'], 200)

    def test_account_get(self):
        print("\nGET /account/")
        
        res = requests.get('http://localhost:8080/account/?type=SIP')
        res = res.json()

        self.assertTrue('status' in res)
        self.assertEqual(res['status'], 200)
        self.assertTrue('details' in res)
        details = res['details']

        self.assertTrue('Account.type' in details)
        self.assertEqual(details['Account.type'], 'SIP')

        res = requests.get('http://localhost:8080/account/?type=IAX')
        res = res.json()

        self.assertTrue('status' in res)
        self.assertEqual(res['status'], 200)
        self.assertTrue('details' in res)
        details = res['details']

        self.assertTrue('Account.type' in details)
        self.assertEqual(details['Account.type'], 'IAX')

        res = requests.get('http://localhost:8080/account/?type=RING')
        res = res.json()

        self.assertTrue('status' in res)
        self.assertEqual(res['status'], 200)
        self.assertTrue('details' in res)
        details = res['details']

        self.assertTrue('Account.type' in details)
        self.assertEqual(details['Account.type'], 'RING')

        res = requests.get('http://localhost:8080/account/?type=stuff')
        res = res.json()

        self.assertTrue('status' in res)
        self.assertEqual(res['status'], 400)
        self.assertFalse('details' in res)

    def test_account_post(self):
        print("\nPOST /account/")
        
        req = requests.get('http://localhost:8080/account/?type=RING')
        req = req.json()
        req['details']['Account.alias'] = "Unittest"
        
        res = requests.post("http://localhost:8080/account/", data=json.dumps(req))
        res = res.json()
      
        self.assertTrue('account_id' in res)
        self.assertTrue('status' in res)
        
        self.test_RING_account = res['account_id']

    def test_account_details_get(self):
        print("\nGET /accounts/<account_id>/details")

        res = requests.get('http://localhost:8080/accounts/')
        res = res.json()
    
        accounts = res['accounts']

        for account in accounts:
            res = requests.get(
                'http://localhost:8080/accounts/' + account + '/details/', 
                {'type' : 'default'}
            )
            res = res.json()
            
            self.assertEqual(res['status'], 200)
            self.assertTrue('details' in res)
       
        print("TODO : implement getVolatileAccountDetails")
#        for account in accounts:
#            res = requests.get(
#                'http://localhost:8080/accounts/' + account + '/details/', 
#                {'type' : 'volatile'}
#            )
#            res = res.json()
#
#            self.assertEqual(res['status'], 200)
    
    def test_account_details_post(self):    
        print("\nPOST /accounts/<account_id>/details")
        
        print("TODO : implement setAccountDetails")

        pass

    def test_account_delete(self):
        print("\nDELETE /accounts/<account_id>")

        res = requests.get('http://localhost:8080/accounts/')
        res = res.json()

        accounts = res['accounts']

        for account in accounts:
            res = requests.get(
                'http://localhost:8080/accounts/' + account + '/details/', 
                {'type':'default'}
            )
            res = res.json()
            
            self.assertEqual(res['status'], 200)
            
            if (res['details']['Account.alias'] == "Unittest"):
                res = requests.delete('http://localhost:8080/accounts/' + account + '/')
                res = res.json()
                self.assertEqual(res['status'], 200)

    def test_account_ciphers_get(self):
        print("\nGET /accounts/<account_id>/ciphers/")

        print("TODO : implement getSupportedCiphers")
        
        pass
    
    def test_account_codecs_get(self):
        print("\nGET /accounts/<account_id>/codecs/")
        
        res = requests.get('http://localhost:8080/accounts/')
        res = res.json()

        accounts = res['accounts']

        for account in accounts:
            res = requests.get('http://localhost:8080/accounts/' + account + '/codecs/')
            res = res.json()
            
            self.assertEqual(res['status'], 200)

    def test_account_codecs_put(self):
        print("\nPUT /accounts/<account_id>/codecs/")

        print("TODO : implement setActiveCodecList")

        pass

    def test_account_codec_details_get(self):
        print("\nGET /accounts/<account_id>/codecs/<codec_id>")
        
        res = requests.get('http://localhost:8080/accounts/')
        res = res.json()

        accounts = res['accounts']

        for account in accounts:
            res = requests.get('http://localhost:8080/accounts/' + account + '/codecs/')
            res = res.json()
            
            self.assertEqual(res['status'], 200)
           
            codecs = res['details']
            
            for codec in codecs:
                res = requests.get(
                    'http://localhost:8080/accounts/' + account + '/codecs/' + str(codec) + '/'
                )
                res = res.json()
                
                self.assertEqual(res['status'], 200)
                self.assertTrue('details' in res)
                     
    def test_account_codec_details_put(self):
        print("\nPUT /accounts/<account_id>/codecs/<codec_id>")

        print("TODO : implement setCodecDetails")

        pass

    
    def test_account_certificates_get(self):
        print("\nGET /accounts/<account_id>/certificates/<cert_id>")
        
        print("TODO : find a way to test validateCertificate")

        pass

    def test_account_certificates_put(self):
        print("\nPUT /accounts/<account_id>/certificates/<cert_id>")

        print("TODO : find a way to test setCertificateStatus")

        pass

class TestCodec(unittest.TestCase):

    def test_codecs(self):
        print("\nGET /codecs/")
        
        res = requests.get('http://localhost:8080/codecs/')
        res = res.json()
    
        self.assertEqual(res['status'], 200)
        self.assertTrue('codecs' in res)
        
class TestCrypto(unittest.TestCase):
    
    def test_crypto_tls(self):
        print("\nGET /crypto/tls/")

        res = requests.get(
            'http://localhost:8080/crypto/tls/', 
            {'type' : 'settings'}
        )
        res = res.json()

        self.assertTrue('settings' in res)
        self.assertTrue('status' in res)

        res = requests.get(
            'http://localhost:8080/crypto/tls/', 
            {'type' : 'method'}
        )
        res = res.json()
                
        self.assertTrue('methods' in res)
        self.assertTrue('status' in res)

class TestCertificates(unittest.TestCase):
   
    def test_certificates_get(self):
        print("\nGET /codecs/")
        
        res = requests.get('http://localhost:8080/certificates/')
        res = res.json()

        self.assertEqual(res['status'], 200)
        self.assertTrue('pinned' in res)

    def test_certificate_get(self):
        print("\nGET /certificate/<cert_id>/")

        print("TODO : find a way to test getPinnedCertificates")

        pass

    def test_certificate_post(self):
        print("\nPOST /certificate/<cert_id>/")

        print("TODO : find a way to test pinCertificate")

        pass

class TestAudio(unittest.TestCase):
   
    def test_audio_plugins_get(self):
        print("\nGET /audio/plugins/")
        
        res = requests.get('http://localhost:8080/audio/plugins/')
        res = res.json()

        self.assertEqual(res['status'], 200)
        self.assertTrue('plugins' in res)
    
class TestVideo(unittest.TestCase):
    
    def test_video_device_get(self):
        print("\nGET /video/devices/")

        res = requests.get(
            'http://localhost:8080/video/devices/', 
            {'type' : 'all'}
        )
        res = res.json()

        self.assertEqual(res['status'], 200)
        self.assertTrue('devices' in res)

        res = requests.get(
            'http://localhost:8080/video/devices/', 
            {'type' : 'default'}
        )
        res = res.json()

        self.assertEqual(res['status'], 200)
        self.assertTrue('default' in res)

    def test_video_device_put(self):
        print("\nPUT /video/devices/")
        
        res = requests.get(
            'http://localhost:8080/video/devices/', 
            {'type' : 'default'}
        )
        res = res.json()
        default = res['default'] 

        params = {'type' : 'default'}
        data = {'device' : default }
        
        res = requests.put(
            'http://localhost:8080/video/devices/', 
            params = params,
            data = json.dumps(data)
        )
        res = res.json()

    def test_video_settings_get(self):
        print("\nGET /video/<device_name>/settings/")
       
        res = requests.get(
            'http://localhost:8080/video/devices/', 
            {'type' : 'default'}
        )
        res = res.json()
        default = res['default'] 

        res = requests.get('http://localhost:8080/video/' + default + '/settings/')
        res = res.json()

        self.assertEqual(res['status'], 200)
        self.assertTrue('settings' in res)

    def test_video_settings_put(self):
        print("\nPUT /video/<device_name>/settings/")
        
        res = requests.get(
            'http://localhost:8080/video/devices/', 
            {'type' : 'default'}
        )
        res = res.json()
        default = res['default'] 

        res = requests.get('http://localhost:8080/video/' + default + '/settings/')
        res = res.json()

        settings = res['settings']

        res = requests.put('http://localhost:8080/video/' + default + '/settings/',
            data = json.dumps({'settings' : settings})
        )
        res = res.json()
        
        self.assertEqual(res['status'], 200)
        self.assertTrue('settings' in res)

    def test_video_camera_get(self):
        print("\nGET /video/camera/")

        res = requests.get('http://localhost:8080/video/camera/')
        res = res.json()

        self.assertEqual(res['status'], 200)
        self.assertTrue('cameraStatus' in res)

    def test_video_camera_put(self):
        print("\nPUT /video/camera/")
        
        res = requests.put('http://localhost:8080/video/camera/', 
            data = json.dumps({'action' : 'start'})
        )
        res = res.json()

        self.assertEqual(res['status'], 200)
        self.assertTrue('cameraStatus' in res)
        
        res = requests.put('http://localhost:8080/video/camera/', 
            data = json.dumps({'action' : 'stop'})
        )
        res = res.json()

        self.assertEqual(res['status'], 200)
        self.assertTrue('cameraStatus' in res)

def TestOrder():    
    suite = unittest.TestSuite()

    suite.addTest(TestAccount('test_account_get'))
    suite.addTest(TestAccount('test_accounts_get'))
    suite.addTest(TestAccount('test_account_post'))
    suite.addTest(TestAccount('test_account_details_get'))
    suite.addTest(TestAccount('test_account_details_post'))
    suite.addTest(TestAccount('test_account_ciphers_get'))
    suite.addTest(TestAccount('test_account_codecs_get'))
    suite.addTest(TestAccount('test_account_codecs_put'))
    suite.addTest(TestAccount('test_account_codec_details_get'))
    suite.addTest(TestAccount('test_account_codec_details_put'))
    suite.addTest(TestAccount('test_account_certificates_get'))
    suite.addTest(TestAccount('test_account_certificates_put'))
    suite.addTest(TestAccount('test_account_delete'))

    suite.addTest(TestCodec('test_codecs'))

    suite.addTest(TestCrypto('test_crypto_tls'))

    suite.addTest(TestCertificates('test_certificates_get'))
    suite.addTest(TestCertificates('test_certificate_get'))
    suite.addTest(TestCertificates('test_certificate_post'))
    
    suite.addTest(TestAudio('test_audio_plugins_get'))
    
    suite.addTest(TestVideo('test_video_device_get'))
    suite.addTest(TestVideo('test_video_device_put'))
    suite.addTest(TestVideo('test_video_settings_get'))
    suite.addTest(TestVideo('test_video_settings_put'))
    suite.addTest(TestVideo('test_video_camera_get'))
    suite.addTest(TestVideo('test_video_camera_put'))

    return suite

if __name__ == '__main__':
    runner = unittest.TextTestRunner(failfast=True)
    runner.run(TestOrder())
