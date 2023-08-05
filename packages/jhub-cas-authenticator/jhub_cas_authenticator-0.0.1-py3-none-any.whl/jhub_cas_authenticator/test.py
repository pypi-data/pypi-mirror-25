#! /usr/bin/env python

import textwrap
from lxml import etree

def main():

    s = textwrap.dedent("""\
    <cas:serviceResponse xmlns:cas='http://www.yale.edu/tp/cas'>
        <cas:authenticationSuccess>
            <cas:user>ballyc</cas:user>
            <cas:attributes>
                <cas:samlAuthenticationStatementAuthMethod>urn:oasis:names:tc:SAML:1.0:am:password</cas:samlAuthenticationStatementAuthMethod>
                <cas:isFromNewLogin>true</cas:isFromNewLogin>
                <cas:authenticationDate>2017-09-16T21:30:35.910-04:00[America/New_York]</cas:authenticationDate>
                <cas:authenticationMethod>LdapAuthenticationHandler</cas:authenticationMethod>
                <cas:surname>Bally</cas:surname>
                <cas:givenName>Cait Lynn</cas:givenName>
                <cas:successfulAuthenticationHandlers>LdapAuthenticationHandler</cas:successfulAuthenticationHandlers>
                <cas:longTermAuthenticationRequestTokenUsed>false</cas:longTermAuthenticationRequestTokenUsed>
                <cas:memberOf>cn=portal-alumni,ou=groups,o=lafayette</cas:memberOf>
                <cas:memberOf>cn=alumni_group,ou=groups,o=lafayette</cas:memberOf>
                <cas:email>LafCaitLynnBally@gmail.com</cas:email>
                </cas:attributes>
        </cas:authenticationSuccess>
    </cas:serviceResponse>
    """)
    parser = etree.XMLParser()
    root = etree.fromstring(s, parser=parser)
    print("root tag: " + root.tag)
    tag = etree.QName(root)
    print("root element namespace: " + tag.namespace)
    print("Tag: " + root[0].tag)
    print("Is success? {0}".format(etree.QName(root[0]).localname == 'authenticationSuccess'))
    print("User: {0}".format(root[0][0].text))
    print("= Attributes =")
    attribs = root[0][1]
    for attrib in attribs:
        name = etree.QName(attrib).localname
        value = attrib.text
        print("* {0}: {1}".format(name, value))

if __name__ == "__main__":
    main()
