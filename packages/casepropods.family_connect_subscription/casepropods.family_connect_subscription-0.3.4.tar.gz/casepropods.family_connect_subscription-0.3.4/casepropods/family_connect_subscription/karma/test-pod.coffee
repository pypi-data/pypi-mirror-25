# Unit tests for our Angular directives

describe('directives:', () ->
  $compile = null
  $rootScope = null
  $templateCache = null
  $q = null
  $filter = null

  beforeEach(() ->
    module('templates')
    module('cases')
    module('templates')

    inject((_$compile_, _$rootScope_, _$templateCache_, _$q_, _$filter_) ->
      $compile = _$compile_
      $rootScope = _$rootScope_
      $templateCache = _$templateCache_
      $q = _$q_
      $filter = _$filter_
    )
  )
  describe('subscriptionPod', () ->
    $rootScope = null
    $compile = null

    beforeEach(inject((_$rootScope_, _$compile_) ->
      $rootScope = _$rootScope_
      $compile = _$compile_

      $rootScope.podConfig = {
            label: 'family_connect_subscription_pod',
            title: 'Subscription Information',
            url: 'http://localhost:8080/api/v1/',
            token: 'a1f16bcb6533ce2cff98e381791bdac65583b343',
        }

      $rootScope.podData = {
        items: []
      }

      $rootScope.status = 'idle'
      $rootScope.trigger = ->
    ))

    it('should draw the pod title', () ->
      $rootScope.podConfig.title = 'Subscription Information'

      el = $compile('<subscription-pod/>')($rootScope)[0]
      $rootScope.$digest()

      expect(el.querySelector('.pod-title').textContent).toMatch(
        'Subscription Information')
    )

    it('should draw when there are no subscriptions', ->
      $rootScope.podData = {
        items: [{ rows: [{
          name: 'No subscriptions', value: ''
        }]}]
      }

      el = $compile('<subscription-pod/>')($rootScope)[0]
      $rootScope.$digest()

      item1 = el.querySelector('.pod-item:nth-child(1)')

      expect(item1.querySelector('.pod-item-name').textContent)
        .toMatch('No subscriptions')

      expect(item1.querySelector('.pod-item-value').textContent)
        .toMatch('')
    )

    it('should draw when there is an error', ->
      $rootScope.podData = {
        items: [{ rows: [{
          name: 'Error', value: 'Bad Request'
        }]}]
      }

      el = $compile('<subscription-pod/>')($rootScope)[0]
      $rootScope.$digest()

      item1 = el.querySelector('.pod-item:nth-child(1)')

      expect(item1.querySelector('.pod-item-name').textContent)
        .toMatch('Error')

      expect(item1.querySelector('.pod-item-value').textContent)
        .toMatch('Bad Request')
    )

    it('should draw when there are subscriptions', ->
      $rootScope.podData = {
        items: [{
          rows: [{
            name: 'Message Set', value: 'test_set'
          }, {
            name: 'Next Sequence Number', value: 1
          }, {
            name: 'Schedule', value: 'At 08:00 every Monday and Tuesday'
          }, {
            name: 'Active', value: 'True'
          }, {
            name: 'Completed', value: 'False'
          }]
        }]
      }

      el = $compile('<subscription-pod/>')($rootScope)[0]
      $rootScope.$digest()

      item1 = el.querySelector('.pod-item:nth-child(1)')
      item2 = el.querySelector('.pod-item:nth-child(2)')
      item3 = el.querySelector('.pod-item:nth-child(3)')
      item4 = el.querySelector('.pod-item:nth-child(4)')
      item5 = el.querySelector('.pod-item:nth-child(5)')

      expect(item1.querySelector('.pod-item-name').textContent)
        .toMatch('Message Set')

      expect(item1.querySelector('.pod-item-value').textContent)
        .toMatch('test_set')

      expect(item2.querySelector('.pod-item-name').textContent)
        .toMatch('Next Sequence Number')

      expect(item2.querySelector('.pod-item-value').textContent)
        .toMatch('1')

      expect(item3.querySelector('.pod-item-name').textContent)
        .toMatch('Schedule')

      expect(item3.querySelector('.pod-item-value').textContent)
        .toMatch('At 08:00 every Monday and Tuesday')

      expect(item4.querySelector('.pod-item-name').textContent)
        .toMatch('Active')

      expect(item4.querySelector('.pod-item-value').textContent)
        .toMatch('True')

      expect(item5.querySelector('.pod-item-name').textContent)
        .toMatch('Completed')

      expect(item5.querySelector('.pod-item-value').textContent)
        .toMatch('False')
    )

    it('should draw the pod actions even if the types aren\'t unique', ->
      $rootScope.podData.actions = [{
        type: 'switch',
        name: 'test_set_1',
        busyText: 'Foo',
        isBusy: false,
        payload: {bar: 'baz'}
      }, {
        type: 'switch',
        name: 'test_set_2',
        busyText: 'Quux',
        isBusy: false,
        payload: {corge: 'grault'}
      }]

      el = $compile('<subscription-pod/>')($rootScope)[0]
      $rootScope.$digest()

      action1 = el.querySelectorAll('.pod-action')[0]
      action2 = el.querySelectorAll('.pod-action')[1]

      expect(action1.textContent).toContain('test_set_1')
      expect(action2.textContent).toContain('test_set_2')
    )
    

    it('should draw whether it is loading', () ->
      $rootScope.status = 'loading'

      el = $compile('<subscription-pod/>')($rootScope)[0]
      $rootScope.$digest()

      expect(el.textContent).toMatch('Loading')
    )

    it('should draw whether loading has failed', () ->
      $rootScope.status = 'loading_failed'

      el = $compile('<subscription-pod/>')($rootScope)[0]
      $rootScope.$digest()

      expect(el.textContent).toMatch('Could not load')
    )
  )
)
