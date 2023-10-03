import i18n from "i18next";
import { initReactI18next } from "react-i18next";

i18n
  .use(initReactI18next)
  .init({
    resources: {
      en: {
        translation: {
          "navGamePlayerNickFinder": "Game Player Nick Finder",
          "navHome": "Home",
          "navCharacters": "Characters",
          "navGames": "Games",
          "navProfile": "Profile",
          "navChangePassword": "Change Password",
          "navAdminPanel": "Admin Panel",
          "navLogOut": "Log Out",
          "navLogIn": "Log In",
          "navRegister": "Register",

          "homeReconnectHeader": "Reconnect with Old Gaming Buddies!",
          "homeReconnectDesc": "Are you missing those unforgettable gaming sessions with your old buddies? Look no further! Our platform is here to help you revive the good old days by reuniting you with your gaming companions. Whether you used to conquer virtual realms together or embark on epic adventures, we bring back the camaraderie and thrill of gaming.",
          "homeJoinNow": "Join now!",
          "homeExplore": "Explore",
          "homeTimeMachine": "Time machine",
          "homeTimeMachineDesc": "Step into the extraordinary world of nostalgia as you reunite with your gaming companions. Embrace your unique synergy and continue the journey of shared excitement and triumphs!",
          "homeFriendship": "Friendship",
          "homeFriendshipDesc": "Rediscover the essence of friendship as you reconnect with old gaming buddies. Forge new alliances and reignite the spirit of camaraderie. Our platform unites players from all corners of the gaming world.",
          "homeFindFriendsHeader": "Find Your Long-Lost Gaming Friends",
          "homeFindFriendsDesc": "Rekindle the gaming magic as you search for your long-lost gaming companions. Our platform is a time machine that takes you back to those cherished moments when you conquered virtual realms and embarked on epic adventures together. Join now and rediscover the joy of gaming camaraderie!",
          "homeSearchNow": "Search Now!",
          "homeJoinAdventure": "Join the Adventure!"

        }
      },
      pl: {
        translation: {
          "navGamePlayerNickFinder": "Game Player Nick Finder",
          "navHome": "Strona główna",
          "navCharacters": "Postacie",
          "navGames": "Gry",
          "navProfile": "Profil",
          "navChangePassword": "Zmień hasło",
          "navAdminPanel": "Panel admina",
          "navLogOut": "Wyloguj",
          "navLogIn": "Zaloguj się",
          "navRegister": "Zarejestruj się",

          "homeReconnectHeader": "Połącz się ponownie ze starymi kumplami z gier!",
          "homeReconnectDesc": "Brakuje ci tych niezapomnianych sesji gier ze starymi przyjaciółmi? Nie szukaj dalej! Nasza platforma pomoże Ci przywrócić dobre stare czasy, łącząc Cię z Twoimi towarzyszami gier. Czy wspólnie podbijaliście wirtualne królestwa, czy wyruszaliście w epickie przygody, przywracamy kameradyzm i emocje gry.",
          "homeJoinNow": "Dołącz teraz!",
          "homeExplore": "Odkrywaj",
          "homeTimeMachine": "Maszyna czasu",
          "homeTimeMachineDesc": "Wejdź do niezwykłego świata nostalgii, łącząc się ponownie z towarzyszami gier. Obejmij swoją unikatową synergię i kontynuuj podróż pełną wspólnego podniecenia i triumfów!",
          "homeFriendship": "Przyjaźń",
          "homeFriendshipDesc": "Odkryj na nowo istotę przyjaźni, łącząc się ponownie ze starymi kumplami z gier. Zawiąż nowe sojusze i rozpal na nowo ducha kameradyzmu. Nasza platforma łączy graczy ze wszystkich zakątków świata gier.",
          "homeFindFriendsHeader": "Znajdź swoich dawno zaginionych przyjaciół z gier",
          "homeFindFriendsDesc": "Ożyw magię gier, szukając swoich dawno zaginionych towarzyszy gier. Nasza platforma to maszyna czasu, która zabiera cię z powrotem do tych cenionych chwil, kiedy podbijaliście wirtualne królestwa i wyruszaliście razem w epickie przygody. Dołącz teraz i odkryj na nowo radość z gier w duchu kameradyzmu!",
          "homeSearchNow": "Szukaj teraz!",
          "homeJoinAdventure": "Dołącz do przygody!"
        }
      }
    },
    lng: "en",
    fallbackLng: "en",
    interpolation: {
      escapeValue: false
    }
  });

export default i18n;
