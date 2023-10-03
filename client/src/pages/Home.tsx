import React from 'react';
import { useTranslation } from 'react-i18next';

const Home: React.FC = () => {
  const { t } = useTranslation();

  return <div>
    <div className={"container my-4"}>
      <div className={"row p-4 pb-0 pe-lg-0 pt-lg-5 align-items-center rounded-3 border shadow-lg mb-2"}>
        <div className={"col-lg-7 p-3 p-lg-5 pt-lg-3"}>
          <h1 className={"display-4 fw-bold lh-1 text-body-emphasis"}>{t('homeReconnectHeader')}</h1>
          <p className={"lead"}>{t('homeReconnectDesc')}</p>
          <div className={"d-grid gap-2 d-md-flex justify-content-md-start mb-4 mb-lg-3"}>
            <a href="{% url 'django_registration_register' %}" role="button" className={"btn btn-primary btn-lg px-4 me-md-2 fw-bold"}>{ t('homeJoinNow') }</a>
            <a href="{% url 'character_list' %}" role="button" className={"btn btn-outline-secondary btn-lg px-4"}>{ t('homeExplore') }</a>
          </div>
        </div>
        <div className={"col-lg-4 offset-lg-1 p-0 overflow-hidden shadow-lg"}>
            <img className={"rounded-lg-3"} src="static/images/friends.jpg" alt="" width="700" />
        </div>
      </div>
    </div>

    <div className={"row align-items-md-stretch"}>
      <div className={"col-md-6"}>
        <div className={"p-4 pb-0 pt-lg-5 align-items-center rounded-3 border shadow-lg p-3 p-lg-5 pt-lg-3"}>
          <h2 className={"display-6 fw-bold lh-1 text-body-emphasis"}>{t('homeTimeMachine')}</h2>
          <p>{t('homeTimeMachineDesc')}</p>
        </div>
      </div>
      <div className={"col-md-6"}>
        <div className={"p-4 pb-0 pt-lg-5 align-items-center rounded-3 border shadow-lg p-3 p-lg-5 pt-lg-3"}>
          <h2 className={"display-6 fw-bold lh-1 text-body-emphasis"}>{t('homeFriendship')}</h2>
          <p>{t('homeFriendshipDesc')}</p>
        </div>
      </div>
    </div>

    <div className={"px-4 pt-5 my-5 text-center"}>{/* border-bottom */}
      <h1 className={"display-4 fw-bold text-body-emphasis"}>{t('homeFindFriendsHeader')}</h1>
      <div className={"col-lg-9 mx-auto"}>
        <p className={"lead mb-4"}>{t('homeFindFriendsDesc')}</p>
        <div className={"d-grid gap-2 d-sm-flex justify-content-sm-center mb-5"}>
          <a href="{% url 'character_list' %}" role="button" className={"btn btn-outline-secondary btn-lg px-4"}>{t('homeSearchNow')}</a>
          <a href="{% url 'django_registration_register' %}" role="button" className={"btn btn-primary btn-lg px-4 me-sm-3"}>{t('homeJoinAdventure')}</a>
        </div>
      </div>
    </div>
      {/* <div className={"overflow-hidden"} style="max-height: 30vh;">
        <div className={"container px-5"}>
          <img src="static/images/together.jpg" className={"img-fluid border rounded-3 shadow-lg mb-4"} alt="Example image" width="700" height="500" loading="lazy" />
        </div> 
      </div> */}

    {/*
    <div className={"container my-5"}>
      <div className={"p-5 text-center bg-body-tertiary rounded-3"}>
        <svg className={"bi mt-4 mb-3"} style="color: var(--bs-indigo);" width="100" height="100"><use xlink:href="#bootstrap"></use></svg>
        <h1 className={"text-body-emphasis"}>Jumbotron with icon</h1>
        <p className={"col-lg-8 mx-auto fs-5 text-muted"}>
          This is a custom jumbotron featuring an SVG image at the top, some longer text that wraps early thanks to a responsive <code>.col-*</code> class, and a customized call to action.
        </p>
        <div className={"d-inline-flex gap-2 mb-5"}>
          <button className={"d-inline-flex align-items-center btn btn-primary btn-lg px-4 rounded-pill"} type="button">
            Call to action
            <svg className={"bi ms-2"} width="24" height="24"><use xlink:href="#arrow-right-short"></use></svg>
          </button>
          <button className={"btn btn-outline-secondary btn-lg px-4 rounded-pill"} type="button">
            Secondary link
          </button>
        </div>
      </div>
    </div>

    <main className={"container py-4"}>
      <div className={"row align-items-md-stretch"}>
        <div className={"col-md-6"}>
          <div className={"h-100 p-5 bg-body-tertiary rounded-3"}>
            <h2>Change the background</h2>
            <p>Swap the background-color utility and add a `.text-*` color utility to mix up the jumbotron look. Then, mix and match with additional component themes and more.</p>
          </div>
        </div>
        <div className={"col-md-6"}>
          <div className={"h-100 p-5 bg-body-tertiary rounded-3"}>
            <h2>Add borders</h2>
            <p>Or, keep it light and add a border for some added definition to the boundaries of your content. Be sure to look under the hood at the source HTML here as we've adjusted the alignment and sizing of both column's content for equal-height.</p>
          </div>
        </div>
      </div>
    </main>

    <div className={"my-5"}>
      <div className={"p-5 text-center bg-body-tertiary"}>
        <div className={"container py-5"}>
          <h1 className={"text-body-emphasis"}>Full-width jumbotron</h1>
          <p className={"col-lg-8 mx-auto lead"}>
            This takes the basic jumbotron above and makes its background edge-to-edge with a <code>.container</code> inside to align content. Similar to above, it's been recreated with built-in grid and utility classes.
          </p>
        </div>
      </div>
    </div>

    <div className={"container col-xxl-8 px-4 py-5"}>
      <div className={"row flex-lg-row-reverse align-items-center g-5 py-5"}>
        <div className={"col-10 col-sm-8 col-lg-6"}>
          <img src="bootstrap-themes.png" className={"d-block mx-lg-auto img-fluid"} alt="Bootstrap Themes" width="700" height="500" loading="lazy" />
        </div>
        <div className={"col-lg-6"}>
          <h1 className={"display-5 fw-bold text-body-emphasis lh-1 mb-3"}>Responsive left-aligned hero with image</h1>
          <p className={"lead"}>Quickly design and customize responsive mobile-first sites with Bootstrap, the world’s most popular front-end open source toolkit, featuring Sass variables and mixins, responsive grid system, extensive prebuilt components, and powerful JavaScript plugins.</p>
          <div className={"d-grid gap-2 d-md-flex justify-content-md-start"}>
            <button type="button" className={"btn btn-primary btn-lg px-4 me-md-2"}>Primary</button>
            <button type="button" className={"btn btn-outline-secondary btn-lg px-4"}>Default</button>
          </div>
        </div>
      </div>
    </div>

    <div className={"px-4 py-5 my-5 text-center"}>
      <img className={"d-block mx-auto mb-4"} src="/docs/5.3/assets/brand/bootstrap-logo.svg" alt="" width="72" height="57" />
      <h1 className={"display-5 fw-bold text-body-emphasis"}>Centered hero</h1>
      <div className={"col-lg-6 mx-auto"}>
        <p className={"lead mb-4"}>Quickly design and customize responsive mobile-first sites with Bootstrap, the world’s most popular front-end open source toolkit, featuring Sass variables and mixins, responsive grid system, extensive prebuilt components, and powerful JavaScript plugins.</p>
        <div className={"d-grid gap-2 d-sm-flex justify-content-sm-center"}>
          <button type="button" className={"btn btn-primary btn-lg px-4 gap-3"}>Primary button</button>
          <button type="button" className={"btn btn-outline-secondary btn-lg px-4"}>Secondary</button>
        </div>
      </div>
    </div>*/}

  </div>;
};

export default Home;
