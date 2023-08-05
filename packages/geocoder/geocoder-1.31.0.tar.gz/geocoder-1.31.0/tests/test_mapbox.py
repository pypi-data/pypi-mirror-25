#!/usr/bin/python
# coding: utf8

import geocoder

location = 'Ottawa, Ontario'
city = 'Ottawa'
ottawa = (45.4215296, -75.6971930)


def test_mapbox():
    g = geocoder.mapbox(location)
    assert g.ok


def test_mapbox_reverse():
    g = geocoder.mapbox(ottawa, method='reverse')
    assert g.ok


def test_multi_results():
    g = geocoder.mapbox(location)
    assert len(g) == 5


def main():
    test_multi_results()

if __name__ == '__main__':
    main()
