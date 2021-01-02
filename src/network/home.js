import { request } from './request'

export function getFilelist () {
  return request({
    url: '/course/filelist',
    method: 'get'
  })
}

export function getMaterials (datas) {
  return request({
    url: '/course/download',
    method: 'post',
    data: datas
  })
}

export function postMaterials (datas) {
  return request({
    url: '/course/upload',
    method: 'post',
    data: datas
  })
}

export function loginByEmail (datas) {
  return request({
    url: '/user/login_by_email',
    method: 'post',
    data: datas
  })
}

export function searchEmail (datas) {
  return request({
    url: '/user/search_email',
    method: 'get',
    data: datas
  })
}

export function getMailVertify (datas) {
  return request({
    url: '/user/get_mail_verify',
    method: 'get',
    data: datas
  })
}

export function checkMailVertify (datas) {
  return request({
    url: '/user/check_mail_verify',
    method: 'post',
    data: datas
  })
}

export function postFilelist (id) {
  return request({
    url: '/course/upvote',
    method: 'post',
    data: id
  })
}

export function postRegister (datas) {
  return request({
    url: '/user/signup',
    method: 'post',
    data: datas
  })
}

export function postLogin (datas) {
  return request({
    url: '/user/login',
    method: 'post',
    data: datas
  })
}

export function postLogout () {
  return request({
    url: '/user/logout',
    method: 'post'
  })
}

export function getddl (datas) {
  return request({
    url: '/schedule/getdeadlinescalendar',
    method: 'post',
    data: datas
  })
}

export function addddl (datas) {
  return request({
    url: '/schedule/addschedule',
    method: 'post',
    data: datas
  })
}

export function delddl (datas) {
  return request({
    url: '/schedule/deleteschedule',
    method: 'post',
    data: datas
  })
}

export function addcourse (datas) {
  return request({
    url: '/course/addCourse',
    method: 'post',
    data: datas
  })
}

export function getcourse (datas) {
  return request({
    url: '/course/courselist',
    method: 'get',
    data: datas
  })
}

export function deletecourse (datas) {
  return request({
    url: '/course/deleteCourse',
    method: 'post',
    data: datas
  })
}
