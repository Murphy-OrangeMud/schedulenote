import { request, request1, request2 } from './request'

export function getHomeMultidata () {
  return request({
    url: '/course/filelist'
  })
}

export function postHomeMultidata (id) {
  return request({
    url: '/course/upvote',
    method: 'post',
    data: id
  })
}

export function postRegister (datas) {
  return request1({
    url: '/user/signup',
    method: 'post',
    data: datas
  })
}

export function postLogin (datas) {
  return request1({
    url: '/user/login',
    method: 'post',
    data: datas
  })
}

export function getddl (datas) {
  return request2({
    url: '/schedule/getdeadlinescalendar',
    method: 'post',
    data: datas
  })
}

export function addddl (datas) {
  return request2({
    url: '/schedule/addschedule',
    method: 'post',
    data: datas
  })
}

export function delddl (datas) {
  return request2({
    url: '/schedule/deleteschedule',
    method: 'post',
    data: datas
  })
}
