# [Taipei-day-trip (Python)](https://taipei-day-trip.beelinetw.com)

Taipei-day-trip is an E-commerce website that offers itinerary reservation, itinerary purchase, and member information.

<br/>

This project built with Python Flask and pure JavaScript, I also have a [Go Gin](https://github.com/Ben10225/GO_tp-d-trip) (GitHub) version for practice.

<br/>

![](https://github.com/Ben10225/taipei-day-trip/blob/develop/public/images/taipei-day-trip-demo.gif)

Here is the testing credit card info for booking page.
|Column| Submit value|
|---|---|
|Card number|4242424242424242|
|Card Expiration|01 / 24|
|Card verification number|123|

## Table of Contents

- [Main Features](#main-features)
- [Backend Technique](#backend-technique)
  - [Framework](#framework)
  - [Infrastructure](#infrastructure)
  - [Database](#database)
  - [Cloud Services](#cloud-services)
  - [Version Control](#version-control)
- [Frontend Technique](#frontend-technique)
- [Architecture](#architecture)
- [Database Schema](#database-schema)
- [Design Doc](#design-doc)

## Main Features

- Member system with JWT token.
- RWD with CSS Grid.
- Infinite scroll / Image carousel.
- Shopping cart system.
- Third-party payment system with TapPay.
- Review history bookings.
- Store images with AWS S3.

## Backend Technique

### Framework

- Python (flask)

### Infrastructure

- DNS
- Nginx
- SSL (Zero SSL)

### Database

- MySQL

### Cloud Services

- EC2

### Version Control

- Git / GitHub

## Frontend Technique

- HTML
- CSS (SCSS)
- JavaScript

## Architecture

<img src="https://github.com/Ben10225/taipei-day-trip/blob/develop/public/images/tp-structure-py.jpg" width=600 />

## Database Schema

<img src="https://github.com/Ben10225/taipei-day-trip/blob/develop/public/images/tp-database.png" width=600 />

## Design Doc

[Figma](https://www.figma.com/file/MZkYBH31H5gyLoZoZq116j)
</br>

[API Doc](https://app.swaggerhub.com/apis-docs/padax/taipei-day-trip/1.1.0)
