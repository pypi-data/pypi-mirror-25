{\rtf1\ansi\ansicpg936\cocoartf1504\cocoasubrtf830
{\fonttbl\f0\fnil\fcharset0 Menlo-Regular;}
{\colortbl;\red255\green255\blue255;\red14\green60\blue38;}
{\*\expandedcolortbl;;\cssrgb\c4706\c29412\c20000;}
\paperw11900\paperh16840\margl1440\margr1440\vieww10800\viewh8400\viewkind0
\deftab720
\pard\pardeftab720\sl280\partightenfactor0

\f0\fs28 \cf2 \expnd0\expndtw0\kerning0
\outl0\strokewidth0 \strokec2 =====\
Polls\
=====\
\
Polls is a simple Django app to conduct Web-based polls. For each\
question, visitors can choose between a fixed number of answers.\
\
Detailed documentation is in the "docs" directory.\
\
Quick start\
-----------\
\
1. Add "polls" to your INSTALLED_APPS setting like this::\
\
    INSTALLED_APPS = (\
        ...\
        'polls',\
    )\
\
2. Include the polls URLconf in your project urls.py like this::\
\
    url(r'^polls/', include('polls.urls')),\
\
3. Run `python manage.py migrate` to create the polls models.\
\
4. Start the development server and visit http://127.0.0.1:8000/admin/\
   to create a poll (you'll need the Admin app enabled).\
\
5. Visit http://127.0.0.1:8000/polls/ to participate in the poll.\
}