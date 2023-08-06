{\rtf1\ansi\ansicpg1252\cocoartf1504\cocoasubrtf830
{\fonttbl\f0\fswiss\fcharset0 Helvetica;\f1\fnil\fcharset0 Menlo-Bold;\f2\fnil\fcharset0 Menlo-Regular;
}
{\colortbl;\red255\green255\blue255;\red0\green0\blue0;\red255\green255\blue255;\red255\green0\blue0;
}
{\*\expandedcolortbl;;\csgenericrgb\c0\c0\c0;\csgenericrgb\c100000\c100000\c100000;\csgenericrgb\c100000\c0\c0;
}
\paperw11900\paperh16840\margl1440\margr1440\vieww16160\viewh8400\viewkind0
\pard\tx566\tx1133\tx1700\tx2267\tx2834\tx3401\tx3968\tx4535\tx5102\tx5669\tx6236\tx6803\pardirnatural\partightenfactor0

\f0\fs24 \cf0 Application name:- 
\b Django-tts-reports
\b0 \
Description:- 
\b This is an application developed for TruTrade Limited . The app enables TruTrade Back office to generate buyer reports that the can share with  buyers \
\

\b0 NB
\b : This application is still under constant improvement and more reports are still being added to the application. 
\b0 \
 
\b \
How to install the reports application \

\b0 \
Dependances \
\pard\tx566\tx1133\tx1700\tx2267\tx2834\tx3401\tx3968\tx4535\tx5102\tx5669\tx6236\tx6803\pardirnatural\partightenfactor0

\f1\b \cf2 \cb3     - easy_pdf\uc0\u8232     - reportlab\u8232     - django.contrib.humanize    - requests
\f0\b0 \cf0 \cb1 \
\
a. Then install the django-tts-reports application \
\
cmd: 
\b \cf2 \cb3 pip install django-tts-reports\
\
\pard\tx560\tx1120\tx1680\tx2240\tx2800\tx3360\tx3920\tx4480\tx5040\tx5600\tx6160\tx6720\pardirnatural\partightenfactor0

\f2\b0 \cf2 b.Include the application in your settings file under installed apps\

\f0 \cf0 \cb1 \
\pard\tx566\tx1133\tx1700\tx2267\tx2834\tx3401\tx3968\tx4535\tx5102\tx5669\tx6236\tx6803\pardirnatural\partightenfactor0

\f2 \cf2 \cb3 INSTALLED_APPS = [\
. . . .   \
\pard\tx566\tx1133\tx1700\tx2267\tx2834\tx3401\tx3968\tx4535\tx5102\tx5669\tx6236\tx6803\pardirnatural\partightenfactor0

\f1\b \cf2 'reports',\
\pard\tx566\tx1133\tx1700\tx2267\tx2834\tx3401\tx3968\tx4535\tx5102\tx5669\tx6236\tx6803\pardirnatural\partightenfactor0

\f2\b0 \cf2 \uc0\u8232 ]\
\pard\tx566\tx1133\tx1700\tx2267\tx2834\tx3401\tx3968\tx4535\tx5102\tx5669\tx6236\tx6803\pardirnatural\partightenfactor0

\f0 \cf0 \cb1 \
c. Add the API domain some where in you the settings file.\
\
\pard\tx566\tx1133\tx1700\tx2267\tx2834\tx3401\tx3968\tx4535\tx5102\tx5669\tx6236\tx6803\pardirnatural\partightenfactor0

\f1\b \cf2 \cb3 API_DOMAIN = 'http://tss.dgitalnatives.com'
\f0\b0 \cf0 \cb1 \
\
d. Add this to  the settings URL file \
\
\pard\tx560\tx1120\tx1680\tx2240\tx2800\tx3360\tx3920\tx4480\tx5040\tx5600\tx6160\tx6720\pardirnatural\partightenfactor0

\f1\b \cf2 \cb3 url(r'^reports/', include('reports.url', namespace='report')),\
\
\pard\tx560\tx1120\tx1680\tx2240\tx2800\tx3360\tx3920\tx4480\tx5040\tx5600\tx6160\tx6720\pardirnatural\partightenfactor0

\f2\b0 \cf2 e.Create a link and pass it 
\f1\b deal_UUID 
\f2\b0 and
\f1\b  full site_domain
\f2\b0  to generated the report. See format below \
\
\pard\tx560\tx1120\tx1680\tx2240\tx2800\tx3360\tx3920\tx4480\tx5040\tx5600\tx6160\tx6720\pardirnatural\partightenfactor0

\f1\b \cf2 [\'91\cf4 site_domain\cf2 \'92]/reports/deal-buyer-report/[\'91\cf4 deal_uuid\cf2 \'92]/
\f2\b0 \
\
example:-  
\f1\b \cf4 http://127.0.0.1:8000\cf2 /reports/deal-buyer-report/\cf4 b57b696d-029e-4b41-b879-58546c304bfb\cf2 /\
\
\pard\tx560\tx1120\tx1680\tx2240\tx2800\tx3360\tx3920\tx4480\tx5040\tx5600\tx6160\tx6720\pardirnatural\partightenfactor0

\f2\b0 \cf2 \

\f0 \cf0 \cb1 \
\
\pard\tx566\tx1133\tx1700\tx2267\tx2834\tx3401\tx3968\tx4535\tx5102\tx5669\tx6236\tx6803\pardirnatural\partightenfactor0
\cf0  }