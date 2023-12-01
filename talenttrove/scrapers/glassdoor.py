import requests
from tqdm import tqdm
import http.cookies
import time

search_params = [
    {
        "operationName": "JobSearchResultsQuery",
        "variables": {
            "excludeJobListingIds": [],
            "filterParams": [],
            "keyword": "software engineer",
            "locationId": 3235921,
            "locationType": "CITY",
            "numJobsToShow": 100,
            "originalPageUrl": "https://www.glassdoor.sg/Job/singapore-software-engineer-jobs-SRCH_IL.0,9_IC3235921_KO10,27.htm",
            "parameterUrlInput": "IL.0,9_IC3235921_KO10,27",
            "seoFriendlyUrlInput": "singapore-software-engineer-jobs",
            "seoUrl": True,
        },
        "query": "query JobSearchResultsQuery($excludeJobListingIds: [Long!], $keyword: String, $locationId: Int, $locationType: LocationTypeEnum, $numJobsToShow: Int!, $pageCursor: String, $pageNumber: Int, $filterParams: [FilterParams], $originalPageUrl: String, $seoFriendlyUrlInput: String, $parameterUrlInput: String, $seoUrl: Boolean) {\n  jobListings(\n    contextHolder: {searchParams: {excludeJobListingIds: $excludeJobListingIds, keyword: $keyword, locationId: $locationId, locationType: $locationType, numPerPage: $numJobsToShow, pageCursor: $pageCursor, pageNumber: $pageNumber, filterParams: $filterParams, originalPageUrl: $originalPageUrl, seoFriendlyUrlInput: $seoFriendlyUrlInput, parameterUrlInput: $parameterUrlInput, seoUrl: $seoUrl, searchType: SR}}\n  ) {\n    filterOptions\n    indeedCtk\n    jobListings {\n      ...JobView\n      __typename\n    }\n    jobListingSeoLinks {\n      linkItems {\n        position\n        url\n        __typename\n      }\n      __typename\n    }\n    jobSearchTrackingKey\n    jobsPageSeoData {\n      pageMetaDescription\n      pageTitle\n      __typename\n    }\n    paginationCursors {\n      cursor\n      pageNumber\n      __typename\n    }\n    indexablePageForSeo\n    searchResultsMetadata {\n      searchCriteria {\n        implicitLocation {\n          id\n          localizedDisplayName\n          type\n          __typename\n        }\n        keyword\n        location {\n          id\n          shortName\n          localizedShortName\n          localizedDisplayName\n          type\n          __typename\n        }\n        __typename\n      }\n      footerVO {\n        countryMenu {\n          childNavigationLinks {\n            id\n            link\n            textKey\n            __typename\n          }\n          __typename\n        }\n        __typename\n      }\n      helpCenterDomain\n      helpCenterLocale\n      jobAlert {\n        jobAlertExists\n        __typename\n      }\n      jobSerpFaq {\n        questions {\n          answer\n          question\n          __typename\n        }\n        __typename\n      }\n      jobSerpJobOutlook {\n        occupation\n        paragraph\n        __typename\n      }\n      showMachineReadableJobs\n      __typename\n    }\n    serpSeoLinksVO {\n      relatedJobTitlesResults\n      searchedJobTitle\n      searchedKeyword\n      searchedLocationIdAsString\n      searchedLocationSeoName\n      searchedLocationType\n      topCityIdsToNameResults {\n        key\n        value\n        __typename\n      }\n      topEmployerIdsToNameResults {\n        key\n        value\n        __typename\n      }\n      topEmployerNameResults\n      topOccupationResults\n      __typename\n    }\n    totalJobsCount\n    __typename\n  }\n}\n\nfragment JobView on JobListingSearchResult {\n  jobview {\n    header {\n    jobLink\n     adOrderId\n    adOrderSponsorshipLevel\n    advertiserType\n    ageInDays\n    applicationId\n    appliedDate\n    applyUrl\n    applyButtonDisabled\n    blur\n    coverPhoto {\n      url\n      __typename\n    }\n    divisionEmployerName\n    easyApply\n    easyApplyMethod\n    employerNameFromSearch\n    employer {\n      activeStatus\n      bestProfile {\n        id\n        __typename\n      }\n      id\n      name\n      shortName\n      size\n      squareLogoUrl\n      __typename\n    }\n      employerNameFromSearch\n      goc\n      gocConfidence\n      gocId\n      jobCountryId\n      jobLink\n      jobResultTrackingKey\n      jobTitleText\n      locationName\n      needsCommission\n      payCurrency\n      payPeriod\n      payPeriodAdjustedPay {\n        p10\n        p50\n        p90\n        __typename\n      }\n      rating\n      salarySource\n      savedJobId\n      sponsored\n      __typename\n    }\n    job {\n      importConfigId\n      jobTitleId\n      jobTitleText\n      listingId\n      __typename\n    }\n    jobListingAdminDetails {\n      cpcVal\n      importConfigId\n      jobListingId\n      jobSourceId\n      userEligibleForAdminJobDetails\n      __typename\n    }\n    job {\n   description\n   }\n overview {\n      shortName\n      squareLogoUrl\n      __typename\n    }\n    __typename\n  }\n  __typename\n}\n",
    }
]

job_param = [
    {
        "operationName": "JobDetailQuery",
        "variables": {
            "enableReviewSummary": True,
            "jl": 1008957268339,
            "queryString": "pos=201&ao=1136043&s=58&guid=0000018c1f75989b9984b595c768a007&src=GD_JOB_AD&t=SR&vt=w&uido=EF3669F859A459101115EA633EFE0CA1&cs=1_5e41da49&cb=1701334850019&jobListingId=1008999847467&jrtk=5-pdx1-0-1hgfnb67bioeb800-71584843a86c205c",
            "pageTypeEnum": "SERP",
        },
        "query": "query JobDetailQuery($jl: Long!, $queryString: String, $enableReviewSummary: Boolean!, $pageTypeEnum: PageTypeEnum) {\n  jobview: jobView(\n    listingId: $jl\n    contextHolder: {queryString: $queryString, pageTypeEnum: $pageTypeEnum}\n  ) {\n    ...DetailFragment\n    employerReviewSummary @include(if: $enableReviewSummary) {\n      reviewSummary {\n        highlightSummary {\n          sentiment\n          sentence\n          categoryReviewCount\n          __typename\n        }\n        __typename\n      }\n      __typename\n    }\n    __typename\n  }\n}\n\nfragment DetailFragment on JobView {\n  employerBenefits {\n    benefitsOverview {\n      benefitsHighlights {\n        benefit {\n          commentCount\n          icon\n          name\n          __typename\n        }\n        highlightPhrase\n        __typename\n      }\n      overallBenefitRating\n      employerBenefitSummary {\n        comment\n        __typename\n      }\n      __typename\n    }\n    benefitReviews {\n      benefitComments {\n        id\n        comment\n        __typename\n      }\n      cityName\n      createDate\n      currentJob\n      rating\n      stateName\n      userEnteredJobTitle\n      __typename\n    }\n    numReviews\n    __typename\n  }\n  employerContent {\n    featuredVideoLink\n    managedContent {\n      id\n      type\n      title\n      body\n      captions\n      photos\n      videos\n      __typename\n    }\n    diversityContent {\n      goals {\n        id\n        workPopulation\n        underRepresentedGroup\n        currentMetrics\n        currentMetricsDate\n        representationGoalMetrics\n        representationGoalMetricsDate\n        __typename\n      }\n      __typename\n    }\n    __typename\n  }\n  employerAttributes {\n    attributes {\n      attributeName\n      attributeValue\n      __typename\n    }\n    __typename\n  }\n  gaTrackerData {\n    isSponsoredFromIndeed\n    isSponsoredFromJobListingHit\n    jobViewDisplayTimeMillis\n    requiresTracking\n    pageRequestGuid\n    searchTypeCode\n    trackingUrl\n    __typename\n  }\n  header {\n    jobLink\n    adOrderId\n    adOrderSponsorshipLevel\n    advertiserType\n    ageInDays\n    applicationId\n    appliedDate\n    applyUrl\n    applyButtonDisabled\n    blur\n    coverPhoto {\n      url\n      __typename\n    }\n    divisionEmployerName\n    easyApply\n    easyApplyMethod\n    employerNameFromSearch\n    employer {\n      activeStatus\n      bestProfile {\n        id\n        __typename\n      }\n      id\n      name\n      shortName\n      size\n      squareLogoUrl\n      __typename\n    }\n    expired\n    goc\n    hideCEOInfo\n    indeedApplyMetadata\n    indeedJobAttribute {\n      education\n      skills\n      educationLabel\n      skillsLabel\n      yearsOfExperienceLabel\n      __typename\n    }\n    isIndexableJobViewPage\n    jobTitleText\n    jobType\n    jobTypeKeys\n    jobCountryId\n    jobResultTrackingKey\n    locId\n    locationName\n    locationType\n    needsCommission\n    normalizedJobTitle\n    organic\n    payCurrency\n    payPeriod\n    payPeriodAdjustedPay {\n      p10\n      p50\n      p90\n      __typename\n    }\n    rating\n    remoteWorkTypes\n    salarySource\n    savedJobId\n    seoJobLink\n    sgocId\n    sponsored\n    categoryMgocId\n    urgencySignal {\n      labelKey\n      messageKey\n      normalizedCount\n      __typename\n    }\n    __typename\n  }\n  similarJobs {\n    relatedJobTitle\n    careerUrl\n    __typename\n  }\n  job {\n    description\n    discoverDate\n    eolHashCode\n    importConfigId\n    jobReqId\n    jobSource\n    jobTitleId\n    jobTitleText\n    listingId\n    __typename\n  }\n  jobListingAdminDetails {\n    adOrderId\n    cpcVal\n    importConfigId\n    jobListingId\n    jobSourceId\n    userEligibleForAdminJobDetails\n    __typename\n  }\n  map {\n    address\n    cityName\n    country\n    employer {\n      id\n      name\n      __typename\n    }\n    lat\n    lng\n    locationName\n    postalCode\n    stateName\n    __typename\n  }\n  overview {\n    ceo {\n      name\n      photoUrl\n      __typename\n    }\n    id\n    name\n    shortName\n    squareLogoUrl\n    headquarters\n    links {\n      overviewUrl\n      benefitsUrl\n      photosUrl\n      reviewsUrl\n      salariesUrl\n      __typename\n    }\n    primaryIndustry {\n      industryId\n      industryName\n      sectorName\n      sectorId\n      __typename\n    }\n    ratings {\n      overallRating\n      ceoRating\n      ceoRatingsCount\n      recommendToFriendRating\n      compensationAndBenefitsRating\n      cultureAndValuesRating\n      careerOpportunitiesRating\n      seniorManagementRating\n      workLifeBalanceRating\n      __typename\n    }\n    revenue\n    size\n    sizeCategory\n    type\n    website\n    yearFounded\n    __typename\n  }\n  photos {\n    photos {\n      caption\n      photoId\n      photoId2x\n      photoLink\n      photoUrl\n      photoUrl2x\n      __typename\n    }\n    __typename\n  }\n  reviews {\n    reviews {\n      advice\n      cons\n      countHelpful\n      employerResponses {\n        response\n        responseDateTime\n        userJobTitle\n        __typename\n      }\n      employmentStatus\n      featured\n      isCurrentJob\n      jobTitle {\n        text\n        __typename\n      }\n      lengthOfEmployment\n      pros\n      ratingBusinessOutlook\n      ratingCareerOpportunities\n      ratingCeo\n      ratingCompensationAndBenefits\n      ratingCultureAndValues\n      ratingOverall\n      ratingRecommendToFriend\n      ratingSeniorLeadership\n      ratingWorkLifeBalance\n      reviewDateTime\n      reviewId\n      summary\n      __typename\n    }\n    __typename\n  }\n  __typename\n}\n",
    }
]


class GlassdoorScraper:
    def __init__(self, cookie, gdtoken) -> None:
        self.url = "https://www.glassdoor.sg/graph"
        cookie = http.cookies.SimpleCookie()
        cookie.load(cookie)
        cookie_dict = {k: v.value for k, v in cookie.items()}
        self.cookie = cookie_dict
        self.gdtoken = gdtoken

    def get_search_data(
        self,
    ):
        search_data = []
        headers = {
            "user-agent": "Mozilla/5.0",
            "gd-csrf-token": self.gdtoken,
        }
        params = search_params
        response = requests.post(
            "https://www.glassdoor.sg/graph",
            headers=headers,
            json=params,
            cookies=self.cookie,
        )
        response.status_code
        search_data.append(response.json())
        count = response.json()[0]["data"]["jobListings"]["totalJobsCount"] // 100
        for page in tqdm(range(2, count + 1)):
            print(page)
            for cursor_obj in response.json()[0]["data"]["jobListings"][
                "paginationCursors"
            ]:
                if cursor_obj["pageNumber"] == page:
                    cursor = cursor_obj["cursor"]
                    break
            params = search_params
            params[0]["variables"]["pageNumber"] = page
            params[0]["variables"]["pageCursor"] = cursor
            response = requests.post(
                "https://www.glassdoor.sg/graph",
                headers=headers,
                json=params,
                cookies=self.cookie,
            )
            response.status_code
            search_data.append(response.json())
        return search_data

    def get_job_data(self, search_data):
        count = 0
        job_data = []
        datas = []
        headers = {
            "user-agent": "Mozilla/5.0",
            "gd-csrf-token": self.gdtoken,
        }
        for data in search_data:
            if data[0] is not None:
                if data[0].get("data", {}).get("jobListings", {}):
                    datas.extend(
                        data[0]
                        .get("data", {})
                        .get("jobListings", {})
                        .get("jobListings", [])
                    )
        params = job_param
        for i in tqdm(datas):
            id = i["jobview"]["job"]["listingId"]
            params[0]["variables"]["jl"] = id
            response = requests.post(
                "https://www.glassdoor.sg/graph",
                headers=headers,
                json=params,
                cookies=self.cookie,
            )
            job_data.append(response.json())
            response.status_code
            count += 1
            if count % 100 == 0:
                print("Sleeping")
                time.sleep(20)
        return job_data
