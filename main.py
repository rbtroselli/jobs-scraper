from post import Post
import time
import random 
from functions import get_driver





urls = [
    'https://www.indeed.com/viewjob?jk=36910c9a332adba3&tk=1h48nq7efkefv800&from=serp&vjs=3',
    'https://it.indeed.com/viewjob?jk=a26c00692b7375f6&q=data+engineer&l=roma%2C+lazio&tk=1h49ji399k9bc801&from=web&advn=9800902453508876&adid=415039914&ad=-6NYlbfkN0Cofn_efFNyQyIJMoryfALnFm4o7ZG60A0JhaR1GZOhq8l5iLhkGyB8bwlO08Kw0ch06glwuecJ9eJX-mfkzmxHWPxBTAihgi0Tmix7KJ-0f0QCL_ilKx0-K3Mk-r9TG-MMiZrDmuU9d2smXm44YJaxeBN45uHSg1KzLG6d0QmTvnKQrcWKfguGS1AyoZV9QkWSaqs9Q-mHG9YFPZTLxTQx3WLg25X2SJsRHi4aNBGIKkyE5SHxxIrORIEA1qiyfHru8XddObyr90hxLH0sKuUHUHUKySZX0C-GNm2bmm0QPfYVQFyCN01n4lJe5A5NxfSG_aZM1_zyTkz-1MZ4MxTq2zBAn5Hf3TcyYeNhQmRq0qzvN0ooe8DSDT3YPVo1iEAiUy_pKAAyi8W0ccac6yuisoXkVZ_Sn29mzIPXT_95N8m1feSn11_F&sjdu=yScPAmwOyYDZZKPZuqyBgNfGgBb7kNicfBO512zG_4-iincHTKgG93zzEZCEiZ-iu2arDYyfojZiYI42MSnZjCGHUtW7bCPGB-p1aWvrRcc&acatk=1h49ji9i6jtsq800&pub=4a1b367933fd867b19b072952f68dceb&xkcb=SoCX-_M3NJvHtgA2jb0KbzkdCdPP&vjs=3'
]

driver = get_driver()

for url in urls:
    post = Post(url, driver)
    post.display()
    time.sleep(random.uniform(1,5))

# gestire qui il csv, piazzarci la roba dell'oggetto post
# usare un file con i search term, assegnare anche il search term al post?

# Close the browser
driver.quit()



