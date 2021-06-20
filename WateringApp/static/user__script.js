import {MDCTopAppBar} from '@material/top-app-bar';


$('document').ready(() =>
{
  // Instantiation
  const topAppBarElement = document.querySelector('.mdc-top-app-bar');
  const topAppBar = new MDCTopAppBar(topAppBarElement);
});
