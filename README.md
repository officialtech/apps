# Google Calendar API
> The Google Calendar API is a RESTful API that can be accessed through explicit HTTP calls or via the Google Client Libraries. The API exposes most of the features available in the Google Calendar Web interface.


## [Event]("https://developers.google.com/calendar/v3/reference/events")
- An event on a calendar containing information such as the title, start and end times, and attendees. Events can be either single events or recurring events. An event is represented by an Event resource.
## [Calendar]("https://developers.google.com/calendar/v3/reference/calendars")
- A collection of events. Each calendar has associated metadata, such as calendar description or default calendar time zone. The metadata for a single calendar is represented by a Calendar resource.
## [Calendar List]("https://developers.google.com/calendar/v3/reference/calendarList")
- A list of all calendars on a user's calendar list in the Calendar UI. The metadata for a single calendar that appears on the calendar list is represented by a CalendarListEntry resource. This metadata includes user-specific properties of the calendar, such as its color or notifications for new events.
## [Setting]("https://developers.google.com/calendar/v3/reference/settings")
    - A user preference from the Calendar UI, such as the user's time zone. A single user preference is represented by a Setting Resource.
## [ACL]("https://developers.google.com/calendar/v3/reference/acl")
- An access control rule granting a user (or a group of users) a specified level of access to a calendar. A single access control rule is represented by an ACL resource.
