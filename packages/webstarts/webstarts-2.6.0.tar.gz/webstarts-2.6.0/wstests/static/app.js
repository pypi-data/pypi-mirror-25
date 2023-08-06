/**
 * @author john
 * @version 6/26/17 3:59 PM
 */

$(document).ready(() => {

  $('#fuck').click(() => {

    $.ajax({
      method: 'POST',
      url: '/save',
      data: { name: 'John', location: 'Boston' }
    })
      .done(msg => {
        console.log('msg', msg)
      })

  })

  $('#fuck2').click(() => {

    $.ajax({
      method: 'POST',
      url: '/save2',
      data: { name: 'John', location: 'Boston' }
    })
      .done(msg => {
        console.log('msg', msg)
      })

  })
})
