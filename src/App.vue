<template>
    <banerPage/>
    <router-view/>
    <footerPage/>
</template>
<script>
    import banerPage from "../src/components/banerPage.vue"
    import footerPage from "../src/components/footerPage.vue"
    export default
    {
        components:
        {
            banerPage,
            footerPage
        }
    }
</script>
<style lang="scss">
@import './style/style.scss';
#app
{
    -webkit-font-smoothing: antialiased;
    -moz-osx-font-smoothing: grayscale;
    color: $main-color;
    font-family: foncik;
}
body
{
    margin: 0;
    background-color: $bg-color;
    font-family: foncik;
}
*
{
    font-family: foncik;
    text-transform: uppercase;
}
</style>
