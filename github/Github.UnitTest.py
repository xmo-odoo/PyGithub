import unittest
import MockMockMock
import httplib
import base64

from Github import Github

class TestCase( unittest.TestCase ):
    def setUp( self ):
        unittest.TestCase.setUp( self )

        self.g = Github( "login", "password" )
        self.b64_userpass = base64.b64encode( "login:password" )
        self.b64_userpass = self.b64_userpass.replace( '\n', '' )

        self.connectionFactory = MockMockMock.Mock( "httplib.HTTPSConnection" )
        self.connection = MockMockMock.Mock( "connection", self.connectionFactory )
        self.response = MockMockMock.Mock( "response", self.connectionFactory )
        
        httplib.HTTPSConnection = self.connectionFactory.object

    def tearDown( self ):
        self.connectionFactory.tearDown()
        unittest.TestCase.tearDown( self )

    def expect( self, verb, url, input, status, responseHeaders, output ):
        self.connectionFactory.expect( "api.github.com", strict = True ).andReturn( self.connection.object )
        self.connection.expect.request( verb, url, input, { "Authorization" : "Basic " + self.b64_userpass } )
        self.connection.expect.getresponse().andReturn( self.response.object )
        self.response.expect.status.andReturn( status )
        self.response.expect.getheaders().andReturn( responseHeaders )
        self.response.expect.read().andReturn( output )
        self.connection.expect.close()

    def testSimpleStatus( self ):
        self.expect( "GET", "/test", "null", 200, [], "" )
        self.assertEqual( self.g._statusRequest( "GET", "/test", None, None ), 200 )

    def testSimpleData( self ):
        self.expect( "GET", "/test", "null", 200, [], '{ "foo": "bar" }' )
        self.assertEqual( self.g._dataRequest( "GET", "/test", None, None ), { "foo" : "bar" } )

unittest.main()