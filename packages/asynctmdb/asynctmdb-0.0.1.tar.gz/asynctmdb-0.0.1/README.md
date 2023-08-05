## Supported methods
In what follows
- "✔" mark means that method is supported, 
but not covered with tests 
(or not completely covered),
- "✘" mark means that method is supported 
and covered with tests.


**ACCOUNT**
-  Get Details
-  Get Created Lists
-  Get Favorite Movies
-  Get Favorite TV Shows
-  Mark as Favorite
-  Get Rated Movies
-  Get Rated TV Shows
-  Get Rated TV Episodes
-  Get Movie Watchlist
-  Get TV Show Watchlist
-  Add to Watchlist

**AUTHENTICATION**
-  ✘ Create Request Token
-  ✘ Create Session
-  ✘ Create Session With Login (deprecated)
-  ✘ Create Guest Session

**CERTIFICATIONS**
-  Get Movie Certifications
-  Get TV Certifications

**CHANGES**
-  Get Movie Change List
-  Get TV Change List
-  Get Person Change List

**COLLECTIONS**
-  Get Details
-  Get Images

**COMPANIES**
-  Get Details
-  Get Movies

**CONFIGURATION**
-  Get API Configuration

**CREDITS**
-  Get Details

**DISCOVER**
-  Movie Discover
-  TV Discover

**FIND**
-  ✘ Find by ID

**GENRES**
-  ✘ Get Movie List
-  ✘ Get TV List
-  Get Movies

**GUEST SESSIONS**
-  Get Rated Movies
-  Get Rated TV Shows
-  Get Rated TV Episodes

**JOBS**
-  Get Jobs

**KEYWORDS**
-  Get Details
-  Get Movies

**LISTS**
-  Get Details
-  Check Item Status
-  Create List
-  Add Movie
-  Remove Movie
-  Clear List
-  Delete List

**MOVIES**
-  ✘ Get Details
-  ✘ Get Account States
-  ✘ Get Alternative Titles
-  ✘ Get Changes
-  ✘ Get Credits
-  ✘ Get Images
-  ✘ Get Keywords
-  ✘ Get Release Dates
-  ✘ Get Videos
-  ✘ Get Translations
-  ✘ Get Recommendations
-  ✘ Get Similar Movies
-  ✘ Get Reviews
-  ✘ Get Lists
-  ✘ Rate Movie
-  ✘ Delete Rating
-  ✘ Get Latest
-  ✘ Get Now Playing
-  ✘ Get Popular
-  ✘ Get Top Rated
-  ✘ Get Upcoming

**NETWORKS**
-  Get Details

**PEOPLE**
-  Get Details
-  Get Movie Credits
-  Get TV Credits
-  Get Combined Credits
-  Get External IDs
-  Get Images
-  Get Tagged Images
-  Get Changes
-  Get Latest
-  Get Popular

**REVIEWS**
-  Get Details

**SEARCH**
-  Search Companies
-  Search Collections
-  Search Keywords
-  Search Movies
-  Multi Search
-  Search People
-  Search TV Shows

**TIMEZONES**
-  Get List

**TV**
-  Get Details
-  Get Account States
-  Get Alternative Titles
-  Get Changes
-  Get Content Ratings
-  Get Credits
-  Get External IDs
-  Get Images
-  Get Keywords
-  Get Recommendations
-  Get Similar TV Shows
-  Get Translations
-  Get Videos
-  Rate TV Show
-  Delete Rating
-  Get Latest
-  Get TV Airing Today
-  Get TV On The Air
-  Get Popular
-  Get Top Rated

**TV SEASONS**
-  Get Details
-  Get Changes
-  Get Account States
-  Get Credits
-  Get External IDs
-  Get Images
-  Get Videos

**TV EPISODES**
-  Get Details
-  Get Changes
-  Get Account States
-  Get Credits
-  Get TV Episode External IDs
-  Get Images
-  Rate TV Episode
-  Delete Rating
-  Get Videos

## Running tests
Plain
```bash
./set-api-key.sh python3 setup.py test
```

Inside `Docker` container
```bash
./set-env.sh docker-compose up
```
