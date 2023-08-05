.. vim: set fileencoding=utf-8 :
.. @author: Pavel Korshunov <Pavel.Korshunov@idiap.ch>
.. @date:   Mon Oct 10 22:06:22 CEST 2016

============
User's Guide
============

This package contains access API and description of the voicePA_ database interface.
It includes Bob_-compliant methods for using the database directly from python with provided protocols.

Genuine data
------------

The genuine (non-attack) data is taken directly from AVspoof_ database and can be used by both 
automatic speaker verification (ASV) and presentation attack detection (PAD) systems. 
The genuine data acquisition process lasted approximately two months with 44 subjects, each participating in 
four different sessions configured in different environmental setups. During each recording session, subjects 
were asked to speak out prepared (read) speech, pass-phrases and free speech recorded with three devices: one 
laptop with high-quality microphone and two mobile phones (iPhone 3GS and Samsung S3). 

Attack data
-----------

Based on the genuine data, 24 types of presentation attacks were generated. Attacks were recorded in 
3 different environments (two typical offices and a large conference room), using 5 different playback 
devices, including built-in laptop speakers, high quality speakers, and three phones: iPhone 3GS, 
iPhone 6S, and Samsung S3, and assuming an ASV system running on either laptop, iPhone 3GS, or Samsung S3. 
In addition to a replay type of attacks (speech is recorded and replayed to the microphone of an ASV system), 
two types of synthetic speech were also replayed: speech synthesis and voice conversion (for the details on 
these algorithms, please refer to the paper below published in BTAS 2015 and describing AVspoof_ database).

Here is the list of all attacks in voicePA_ database::

    r106-iphone3gs-laptop-iphone6s
    r106-iphone3gs-samsungs3-samsungs3
    r106-iphone3gs-ss-iphone6s
    r106-iphone3gs-vc-iphone6s
    r106-samsungs3-iphone3gs-iphone3gs
    r106-samsungs3-laptop-iphone6s
    r106-samsungs3-ss-iphone6s
    r106-samsungs3-vc-iphone6s
    r107-laptop-iphone3gs-iphone3gs
    r107-laptop-laptop-hqspeaker
    r107-laptop-laptop-laptop
    r107-laptop-samsungs3-samsungs3
    r107-laptop-ss-hqspeaker
    r107-laptop-ss-laptop
    r107-laptop-vc-hqspeaker
    r107-laptop-vc-laptop
    seboffice-iphone3gs-laptop-iphone6s
    seboffice-iphone3gs-samsungs3-samsungs3
    seboffice-iphone3gs-ss-iphone6s
    seboffice-iphone3gs-vc-iphone6s
    seboffice-samsungs3-iphone3gs-iphone3gs
    seboffice-samsungs3-laptop-iphone6s
    seboffice-samsungs3-ss-iphone6s
    seboffice-samsungs3-vc-iphone6s

The names of these attacks can be interpreted as following: [environment name]-[devices where ASV system is
running]-[type of attack data]-[device of the attack].

Environment represents the place where the attacks were recorded and includes::

    r106 - a large conference room with echo and constant background noise from air-conditioning unit.
    r107 - a small corner office
    seboffice - a larger office with background noise from the wind outside, occasional cars and birds.

Devices where ASV was running are::

    laptop - all the attacks recorded with laptop are copied directly from AVspoof database and correspond
    to replay and physical access attacks in AVspoof.
    iphone3gs - an ASV system is assumed to be running on iPhone 3GS, it means the standard microphone of
    the iPhone 3GS is used to record attacks.
    samsungs3 - similar to the above, attacks are recorded using microphone of Samsung S3 phone.

Type of attack data include::

    replay attacks - created by playing back either the data recorded with 'laptop' or both 'iphone3gs' and 'samsungs3' phones.
    ss - data generated with speech synthesis algorithm
    vc - data generated with voice conversion algorithm

The attacks devices that are used to play back the attack data::

    laptop - internal speakers of the laptop (see 'replay_laptop' and 'physical_access' attacks from AVspoof database)
    hqspeaker - high quality speakers connected to the laptop (see 'replay_laptop_HQ' and 'physical_access_HQ'
    attacks from AVspoof database)
    iphone3gs - iPhone 3GS was used to playback the data.
    samsungs3 - Samsung S3 was used to playback the data.
    iphone6s - iPhone 6S was used to playback the data.

Protocols
---------

The data in voicePA_ database is split into three non-overlapping subsets: training (genuine and attack
samples from 4 female and 4 male subjects), development or 'Dev'  (genuine and attack samples from 4 female
and 10 male subjects), and evaluation or 'Eval'  (genuine and attack samples from 5 female and 11 male subjects).

Within these train, dev, and eval sets, the following protocols are provided:
    'grandtest' - all genuine and attack data are included in this protocol. 
    'smalltest' - a small subset of genuine and attack data (only one subject for each train, dev, and eval sets).
    This protocol should be used for debugging purposes only.
    'avspoofPA' - this protocol includes all genuine data and the presentation attack data from AVspoof_
    database (corresponding to 'physical_access' attacks).
    'r106' - all genuine data and all attacks recorded in the large conference room.
    'seboffice' - all genuine data and all attacks recorded in the office room.
    'replay' - all genuine and replay attacks of natural speech (no 'ss' and 'vc' data).
    'synthetic' - all genuine and synthetic speech only ('ss' and 'vc' data), hence no replay attacks
    of a natural speech.
    'mobile' - all genuine and attacks on ASV systems running on mobile devices, which means target devices
    are iPhone 3GS and Samsung S3.
    'samsungs3' - all genuine and attacks only for Samsung S3 device (ASV system is assumed to be running
    on this device only).
    'iphone3gs' - all genuine and attacks only for iPhone 3GS device (ASV system is assumed to be running
    on this device only).


.. _bob: https://www.idiap.ch/software/bob
.. _voicePA: https://www.idiap.ch/dataset/voicepa
.. _AVspoof: https://www.idiap.ch/dataset/avspoof

