import { ref } from 'vue'
import Shepherd from 'shepherd.js'
import { useRouter } from 'vue-router'

export function useTutorial() {
  const router = useRouter()
  const isActive = ref(false)

  const createTour = (searchForSuburb?: (query: string) => Promise<void>) => {
    const tour = new Shepherd.Tour({
      useModalOverlay: true,
      defaultStepOptions: {
        classes: 'shepherd-theme-hotspot',
        scrollTo: false,
        modalOverlayOpeningPadding: 8
      }
    })

    // The entire tutorial experience is not very good on mobile, this is
    // so that it doesn't bind to particular elements.
    const isMobile = () => window.innerWidth < 768

    const createAttachment = (element: string, position: string) => {
      return isMobile() ? undefined : { element, on: position }
    }

    const wait = (ms: number) => new Promise((resolve) => setTimeout(resolve, ms))

    const createButtons = (showBack = true, backAction?: () => void, nextText = 'Next', nextAction?: () => void) => [
      ...(showBack ? [{
        text: 'Back',
        classes: 'shepherd-button-secondary',
        action: backAction || (() => tour.back())
      }] : []),
      {
        text: nextText,
        classes: 'shepherd-button-primary',
        action: nextAction || (() => tour.next())
      }
    ]


    tour.addStep({
      title: 'Welcome to Hotspot',
      text: 'This tutorial will guide you through the key features of Hotspot - your guide to safe motorbike parking in Victoria',
      buttons: createButtons(false, undefined, 'Skip', () => tour.complete()).concat([{
        text: 'Next',
        classes: 'shepherd-button-primary',
        action: () => tour.next()
      }])
    })

    tour.addStep({
      title: 'Search for Suburbs',
      text: 'Let me show you how it works by searching for "Melbourne". Watch as I type it in!',
      attachTo: createAttachment('.hero-search-bar', 'bottom'),
      buttons: createButtons(true, undefined, 'Type Melbourne', async () => {
        if (searchForSuburb) {
          await searchForSuburb('Melbourne')
          tour.next()
        } else {
          tour.next()
        }
      })
    })

    tour.addStep({
      title: 'Safety Score',
      text: 'This safety score (0-100) shows how secure Melbourne is for parking, based on real theft data. Higher scores mean safer areas.',
      attachTo: createAttachment('[data-testid="safety-score"]', 'right'),
      buttons: createButtons(true, () => {
        router.push('/')
        tour.back()
      })
    })

    tour.addStep({
      title: 'Community Parking Spots',
      text: 'The Parking Feed shows secure spots shared by other riders in this area. Look for well-lit areas and security features.',
      attachTo: createAttachment('.v-tabs-window-item:first-child', 'top'),
      buttons: createButtons()
    })

    tour.addStep({
      title: 'Nearest Suburbs',
      text: 'Let me show you the nearby suburbs and their safety scores. This helps you find alternative parking areas.',
      attachTo: createAttachment('.v-tab:nth-child(2)', 'bottom'),
      buttons: [
        {
          text: 'Back',
          classes: 'shepherd-button-secondary',
          action: () => tour.back()
        },
        {
          text: 'Show Nearest Suburbs',
          classes: 'shepherd-button-primary',
          action: () => {
            // Click the Nearest Suburbs tab
            const nearestSuburbsTab = document.querySelector('.v-tab:nth-child(2)') as HTMLElement
            if (nearestSuburbsTab) {
              nearestSuburbsTab.click()
            }
            setTimeout(() => tour.next(), 500)
          }
        }
      ]
    })

    tour.addStep({
      title: 'Safety Trends',
      text: 'Now let me show you the trends data - theft patterns over time that help you understand if an area is getting safer or more dangerous.',
      attachTo: createAttachment('.v-tab:nth-child(3)', 'bottom'),
      buttons: [
        {
          text: 'Back',
          classes: 'shepherd-button-secondary',
          action: () => {
            // Go back to Nearest Suburbs tab
            const nearestSuburbsTab = document.querySelector('.v-tab:nth-child(2)') as HTMLElement
            if (nearestSuburbsTab) {
              nearestSuburbsTab.click()
            }
            tour.back()
          }
        },
        {
          text: 'Show Trends',
          classes: 'shepherd-button-primary',
          action: () => {
            // Click the Trends tab
            const trendsTab = document.querySelector('.v-tab:nth-child(3)') as HTMLElement
            if (trendsTab) {
              trendsTab.click()
            }
            setTimeout(() => tour.next(), 500)
          }
        }
      ]
    })

    tour.addStep({
      title: 'Share Your Parking Spot',
      text: 'Found a great secure spot? Click here to share it with the community. Add details about lighting, security, and nearby facilities.',
      attachTo: createAttachment('[data-testid="parking-add-button"]', 'left'),
      beforeShowPromise: async () => {
        // Make sure we're on a suburb page (Melbourne from step 2)
        const currentPath = router.currentRoute.value.path
        if (!currentPath.includes('/suburb/')) {
          // Go back to Melbourne which was searched in step 2
          await router.push('/suburb/melbourne-3000')
          await wait(500)
        }

        // Click the Parking Feed tab to ensure we're on the right tab
        const parkingFeedTab = document.querySelector('[data-testid="parking-feed-tab"]') as HTMLElement | null
        if (parkingFeedTab) {
          parkingFeedTab.click()
          await wait(300)
        }

        // Wait for the Add Location button to appear and scroll to it
        for (let attempt = 0; attempt < 10; attempt++) {
          const addButton = document.querySelector('[data-testid="parking-add-button"]') as HTMLElement | null
          if (addButton && addButton.offsetParent !== null) {
            addButton.scrollIntoView({ block: 'center', behavior: 'smooth' })
            break
          }
          await wait(200)
        }
      },
      buttons: createButtons()
    })

    tour.addStep({
      title: 'Navigate the App',
      text: 'Use the navigation bar to access different sections. Home brings you back to the search page.',
      attachTo: createAttachment('a[href="/"]', 'bottom'),
      buttons: createButtons()
    })

    tour.addStep({
      title: 'Explore',
      text: 'View suburbs ranked by safety score to find the safest places to park your bike.',
      attachTo: createAttachment('a[href="/explore"]', 'bottom'),
      buttons: createButtons(true, undefined, 'Visit Page', () => {
        router.push('/explore')
        tour.next()
      })
    })

    tour.addStep({
      title: 'Explore Safety Rankings',
      text: 'Here you can filter by postcode or Council, sort by safety score, and explore the safest areas in Victoria.',
      attachTo: createAttachment('.v-data-table', 'top'),
      buttons: [
        {
          text: 'Back',
          classes: 'shepherd-button-secondary',
          action: () => {
            router.push('/')
            tour.back()
          }
        },
        {
          text: 'Next',
          classes: 'shepherd-button-primary',
          action: () => {
            router.push('/saved')
            tour.next()
          }
        }
      ]
    })

    tour.addStep({
      title: 'Saved Parking',
      text: 'This page shows your saved parking locations. You can save spots by clicking the star icon on parking locations.',
      buttons: [
        {
          text: 'Back',
          classes: 'shepherd-button-secondary',
          action: () => {
            router.push('/explore')
            tour.back()
          }
        },
        {
          text: 'Continue Tour',
          classes: 'shepherd-button-primary',
          action: () => {
            router.push('/')
            tour.next()
          }
        }
      ]
    })

    tour.addStep({
      title: 'More Options',
      text: 'Click here to access additional features like Resources, Settings, and Contact information.',
      attachTo: createAttachment('button[aria-haspopup="menu"]', 'left'),
      buttons: createButtons(true, () => {
        router.push('/saved')
        tour.back()
      })
    })

    tour.addStep({
      title: 'You\'re Ready!',
      text: 'Start exploring Victoria\'s safest parking spots and contribute to the community by sharing your discoveries.',
      buttons: createButtons(true, undefined, 'Get Started', () => tour.complete())
    })

    const totalSteps = tour.steps.length
    tour.steps.forEach((step, index) => {
      const originalTitle = step.options?.title
      const numberedTitle = () => {
        const resolvedTitle =
          typeof originalTitle === 'function'
            ? originalTitle.call(step)
            : originalTitle ?? ''
        return resolvedTitle
          ? `${index + 1}/${totalSteps} ${resolvedTitle}`
          : `${index + 1}/${totalSteps}`
      }

      step.updateStepOptions({
        title: numberedTitle
      })
    })

    tour.on('complete', () => {
      isActive.value = false
    })

    tour.on('cancel', () => {
      isActive.value = false
    })

    return tour
  }

  const startTutorial = (searchForSuburb?: (query: string) => Promise<void>) => {
    isActive.value = true
    const tour = createTour(searchForSuburb)
    tour.start()
  }

  return {
    startTutorial,
    isActive
  }
}
