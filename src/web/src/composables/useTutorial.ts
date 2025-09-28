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

    const navigateAndBack = (path: string) => () => {
      router.push(path)
      tour.back()
    }

    const navigateAndNext = (path: string) => () => {
      router.push(path)
      tour.next()
    }

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
      text: 'Found a great secure spot? Use this form to share it with the community. Add details about lighting, security, and nearby facilities.',
      attachTo: createAttachment('.v-sheet:has([data-testid="parking-form"])', 'left'),
      buttons: [
        {
          text: 'Back',
          classes: 'shepherd-button-secondary',
          action: () => tour.back()
        },
        {
          text: 'Next',
          classes: 'shepherd-button-primary',
          action: () => tour.next()
        }
      ]
    })

    tour.addStep({
      title: 'Navigate the App',
      text: 'Use the navigation bar to access different sections. Home brings you back to the search page.',
      attachTo: createAttachment('a[href="/"]', 'bottom'),
      buttons: [
        {
          text: 'Back',
          classes: 'shepherd-button-secondary',
          action: () => tour.back()
        },
        {
          text: 'Next',
          classes: 'shepherd-button-primary',
          action: () => tour.next()
        }
      ]
    })

    tour.addStep({
      title: 'Top Suburbs',
      text: 'View suburbs ranked by safety score to find the safest places to park your bike.',
      attachTo: createAttachment('a[href="/top-suburbs"]', 'bottom'),
      buttons: [
        {
          text: 'Back',
          classes: 'shepherd-button-secondary',
          action: () => tour.back()
        },
        {
          text: 'Visit Page',
          classes: 'shepherd-button-primary',
          action: () => {
            router.push('/top-suburbs')
            tour.next()
          }
        }
      ]
    })

    tour.addStep({
      title: 'Explore Safety Rankings',
      text: 'Here you can filter by postcode or LGA, sort by safety score, and explore the safest areas in Victoria.',
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
            router.push('/top-suburbs')
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
      buttons: [
        {
          text: 'Back',
          classes: 'shepherd-button-secondary',
          action: () => {
            router.push('/saved')
            tour.back()
          }
        },
        {
          text: 'Next',
          classes: 'shepherd-button-primary',
          action: () => tour.next()
        }
      ]
    })

    tour.addStep({
      title: 'You\'re Ready!',
      text: 'You\'ve seen how to search suburbs, explore the navigation, and view safety data. Start exploring Victorias safest parking spots and contribute to the community by sharing your discoveries.',
      buttons: [
        {
          text: 'Back',
          classes: 'shepherd-button-secondary',
          action: () => tour.back()
        },
        {
          text: 'Get Started',
          classes: 'shepherd-button-primary',
          action: () => tour.complete()
        }
      ]
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
